from flask import (
    Blueprint,
    request,
    session,
    render_template,
    redirect,
    url_for,
    flash
)

from datetime import datetime

from extensions import db

from models.user import User
from models.otp_log import OtpLog

from services.auth_service import hash_password

from services.otp_service import create_sms_otp_for_user

from flask_login import (
    login_user,
    logout_user
)


auth_bp = Blueprint(
    "auth",
    __name__
)



# ======================================================
# REGISTER
# ======================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():


    if request.method == "GET":

        return render_template(
            "auth/register.html"
        )



    action = request.form.get(
        "action"
    )


    name = request.form.get(
        "name"
    )

    email = request.form.get(
        "email"
    )

    phone = request.form.get(
        "phone"
    )

    password = request.form.get(
        "password"
    )

    confirm_password = request.form.get(
        "confirm_password"
    )

    role = request.form.get(
        "role",
        "BUYER"
    )

    otp_code = request.form.get(
        "otp_code"
    )


    form_data = request.form



    # ==================================================
    # STEP 1 : SEND OTP
    # ==================================================

    if action == "send_otp":


        if not all([
            name,
            email,
            phone,
            password,
            confirm_password
        ]):


            return render_template(
                "auth/register.html",
                error="Please fill all fields.",
                form=form_data,
                otp_sent=False
            )



        if password != confirm_password:


            return render_template(
                "auth/register.html",
                error="Passwords do not match.",
                form=form_data,
                otp_sent=False
            )



        if role not in [
            "BUYER",
            "FARMER",
            "DELIVERY"
        ]:


            return render_template(
                "auth/register.html",
                error="Invalid role.",
                form=form_data,
                otp_sent=False
            )



        existing_user = User.query.filter_by(
            email=email,
            is_approved=True
        ).first()



        if existing_user:


            return render_template(
                "auth/register.html",
                error="Email already registered.",
                form=form_data,
                otp_sent=False
            )




        # create temporary user

        user = User.query.filter_by(
            email=email
        ).first()



        if not user:


            user = User(

                name=name,

                email=email,

                phone=phone,

                role=role,

                password_hash=hash_password(
                    password
                ),

                is_active=True,

                is_approved=False

            )


            db.session.add(
                user
            )

            db.session.commit()



        else:


            user.name = name

            user.phone = phone

            user.role = role

            user.password_hash = hash_password(
                password
            )


            db.session.commit()



        # SEND OTP HERE

        create_sms_otp_for_user(
            user.id
        )



        return render_template(
            "auth/register.html",

            form=form_data,

            otp_sent=True,

            email=email,

            phone=phone
        )





    # ==================================================
    # STEP 2 : VERIFY OTP
    # ==================================================

    if action == "register":



        if not all([
            name,
            email,
            phone,
            password,
            confirm_password,
            otp_code
        ]):


            return render_template(
                "auth/register.html",

                error="Enter OTP.",

                form=form_data,

                otp_sent=True
            )




        user = User.query.filter_by(
            email=email
        ).first()



        if not user:


            return render_template(
                "auth/register.html",

                error="User not found.",

                form=form_data,

                otp_sent=False
            )





        otp = (

            OtpLog.query

            .filter_by(
                user_id=user.id,
                is_used=False
            )

            .order_by(
                OtpLog.created_at.desc()
            )

            .first()

        )




        if not otp:


            return render_template(
                "auth/register.html",

                error="OTP not generated.",

                form=form_data,

                otp_sent=True
            )




        if datetime.utcnow() > otp.expires_at:


            return render_template(
                "auth/register.html",

                error="OTP expired.",

                form=form_data,

                otp_sent=True
            )





        if otp.otp_code != otp_code:


            return render_template(
                "auth/register.html",

                error="Invalid OTP.",

                form=form_data,

                otp_sent=True
            )





        # OTP SUCCESS


        otp.is_used = True


        user.is_approved = True


        user.is_active = True



        db.session.commit()




        # LOGIN USER

        login_user(
            user
        )



        session["user_id"] = user.id

        session["role"] = user.role




        flash(
            "Account created successfully!",
            "success"
        )



        return redirect(
            url_for(
                "main.home"
            )
        )





    return render_template(
        "auth/register.html"
    )





# ======================================================
# LOGIN
# ======================================================


@auth_bp.route(
    "/login",
    methods=[
        "GET",
        "POST"
    ]
)

def login():


    if request.method == "POST":


        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )



        user = User.query.filter_by(
            email=email
        ).first()



        from werkzeug.security import check_password_hash



        if not user or not check_password_hash(
            user.password_hash,
            password
        ):


            flash(
                "Invalid email or password",
                "danger"
            )

            return render_template(
                "auth/login.html"
            )





        login_user(
            user
        )



        session["user_id"] = user.id

        session["role"] = user.role





        if user.role == "BUYER":

            return redirect(
                url_for(
                    "buyer.dashboard"
                )
            )


        elif user.role == "FARMER":

            return redirect(
                url_for(
                    "farmer.dashboard"
                )
            )


        elif user.role == "DELIVERY":

            return redirect(
                url_for(
                    "delivery.dashboard"
                )
            )


        elif user.role == "ADMIN":

            return redirect(
                url_for(
                    "admin.dashboard"
                )
            )



    return render_template(
        "auth/login.html"
    )





# ======================================================
# LOGOUT
# ======================================================


@auth_bp.route("/logout")
def logout():


    logout_user()


    session.clear()


    flash(
        "Logged out successfully",
        "success"
    )


    return redirect(
        url_for(
            "main.home"
        )
    )