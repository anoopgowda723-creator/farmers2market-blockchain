from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from datetime import datetime

from extensions import db
from models.user import User
from models.otp_log import OtpLog
from services.auth_service import hash_password, verify_password
from services.otp_service import create_sms_otp_for_user
from flask_login import login_user, logout_user, current_user

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

               # Create OTP and send via SMS only
        create_sms_otp_for_user(user.id)

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
    from models.user import User
    from werkzeug.security import check_password_hash
    from flask import request, render_template, redirect, url_for, flash, session

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", form=request.form)

        if not user.is_active:
            flash("Your account is not active yet. Please wait for admin approval.", "warning")
            return render_template("auth/login.html", form=request.form)

        # 🔹 This is the KEY step
        login_user(user)  # tells Flask-Login "this is the logged in user"

        # (optional) keep your old session-based values if you still use them
        session["user_id"] = user.id
        session["role"] = user.role

        # redirect based on role
        if user.role == "ADMIN":
            return redirect(url_for("admin.dashboard"))
        elif user.role == "FARMER":
            return redirect(url_for("farmer.dashboard"))
        elif user.role == "BUYER":
            return redirect(url_for("buyer.dashboard"))
            # or "buyer.shop" etc.
        elif user.role == "DELIVERY":
            return redirect(url_for("delivery.dashboard"))
        else:
            return redirect(url_for("main.home"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    from flask import session, redirect, url_for, flash

    logout_user()      # Flask-Login clear
    session.clear()    # your custom session usage
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))
