from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from datetime import datetime

from extensions import db
from models.user import User
from models.otp_log import OtpLog
from services.auth_service import hash_password, verify_password
from services.otp_service import create_otp_for_user_all_channels

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Single page, two-step flow:
    1) User fills email + phone (+ other fields) and clicks "Verify Email & Phone"
       -> send OTP, show OTP input below email/phone
    2) User enters OTP and clicks "Create Account"
       -> verify OTP, finish registration
    """
    if request.method == "GET":
        return render_template("auth/register.html")

    # Action decides what we do
    action = request.form.get("action", "register")

    # Common form fields
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    role = request.form.get("role", "BUYER")
    otp_code = request.form.get("otp_code")  # may be empty in first step

    form_data = request.form  # to refill values in template
    error = None
    otp_error = None

    # ---------- STEP 1: SEND OTP ----------
    if action == "send_otp":
        if not all([name, email, phone, password, confirm_password]):
            error = "Please fill all fields before verifying."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif role not in ("BUYER", "FARMER", "DELIVERY"):
            error = "Please select a valid role."
        elif User.query.filter_by(email=email, is_approved=True).first():
            error = "Email is already registered."
        elif User.query.filter_by(phone=phone, is_approved=True).first():
            error = "Phone number is already registered."

        if error:
            return render_template(
                "auth/register.html",
                error=error,
                form=form_data,
                otp_sent=False,
            ), 400

        # See if there is an existing unapproved user with this email
        user = User.query.filter_by(email=email, is_approved=False).first()

        if not user:
            # Create a temporary user in "pending verification" state
            user = User(
                name=name,
                email=email,
                phone=phone,
                role=role,
                password_hash=hash_password(password),
                is_active=True,
                is_approved=False,
            )
            db.session.add(user)
            db.session.commit()
        else:
            # Update fields in case user re-tried
            user.name = name
            user.phone = phone
            user.role = role
            user.password_hash = hash_password(password)
            db.session.commit()

        # Create OTP and send to email + phone
        create_otp_for_user_all_channels(user.id)

        return render_template(
            "auth/register.html",
            form=form_data,
            otp_sent=True,
            email=email,
            phone=phone,
        )

    # ---------- STEP 2: COMPLETE REGISTRATION (VERIFY OTP) ----------
    if action == "register":
        if not all([name, email, phone, password, confirm_password, otp_code]):
            error = "Please fill all fields and enter OTP."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif role not in ("BUYER", "FARMER", "DELIVERY"):
            error = "Please select a valid role."

        if error:
            return render_template(
                "auth/register.html",
                error=error,
                form=form_data,
                otp_sent=True,  # keep OTP UI visible
                email=email,
                phone=phone,
            ), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            otp_error = "No pending account found. Please verify again."
            return render_template(
                "auth/register.html",
                form=form_data,
                otp_sent=True,
                email=email,
                phone=phone,
                otp_error=otp_error,
            ), 404

        if user.phone != phone:
            otp_error = "Phone number does not match what you used earlier."
            return render_template(
                "auth/register.html",
                form=form_data,
                otp_sent=True,
                email=email,
                phone="",
                otp_error=otp_error,
            ), 400

        # Get latest unused OTP
        otp_log = (
            OtpLog.query
            .filter_by(user_id=user.id, is_used=False)
            .order_by(OtpLog.created_at.desc())
            .first()
        )

        if not otp_log:
            otp_error = "No active OTP found. Please click 'Verify Email & Phone' again."
            return render_template(
                "auth/register.html",
                form=form_data,
                otp_sent=True,
                email=email,
                phone=phone,
                otp_error=otp_error,
            ), 400

        now = datetime.utcnow()
        if now > otp_log.expires_at:
            otp_error = "OTP has expired. Please verify again."
            return render_template(
                "auth/register.html",
                form=form_data,
                otp_sent=True,
                email=email,
                phone=phone,
                otp_error=otp_error,
            ), 400

        if otp_log.otp_code != otp_code:
            otp_error = "Invalid OTP. Please try again."
            return render_template(
                "auth/register.html",
                form=form_data,
                otp_sent=True,
                email=email,
                phone=phone,
                otp_error=otp_error,
            ), 400

        # OTP is valid → mark used and approve user
        otp_log.is_used = True
        user.is_approved = True
        user.is_active = True
        db.session.commit()

        # Auto login
        session["user_id"] = user.id
        session["user_role"] = user.role

        return redirect(url_for("main.home"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Render login page on GET, handle form submit on POST."""
    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    error = None

    if not email or not password:
        error = "Please enter email and password."
    else:
        user = User.query.filter_by(email=email).first()
        if not user or not verify_password(password, user.password_hash):
            error = "Invalid email or password."
        elif not user.is_active:
            error = "Your account is inactive. Contact support."
        elif not user.is_approved:
            error = "Your account is not verified yet. Please complete OTP verification."

    if error:
        return render_template("auth/login.html", error=error, form=request.form), 401

    session["user_id"] = user.id
    session["user_role"] = user.role
    return redirect(url_for("main.home"))


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200
