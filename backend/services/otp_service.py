import random
from datetime import datetime, timedelta

from models import OtpLog
from extensions import db


def generate_otp():
    """
    Generate 6 digit OTP
    """
    return str(random.randint(100000, 999999))


def create_sms_otp_for_user(user_id):
    """
    Create OTP record for user
    """

    otp = generate_otp()

    otp_record = OtpLog(
        user_id=user_id,
        channel="SMS",
        otp_code=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.session.add(otp_record)
    db.session.commit()

    # Development testing output
    print(f"[OTP GENERATED] User ID: {user_id} OTP: {otp}")

    return otp



def verify_otp(user_id, otp):
    """
    Verify user OTP
    """

    record = OtpLog.query.filter_by(
        user_id=user_id,
        otp_code=otp,
        is_used=False
    ).first()


    if not record:
        return False


    if record.expires_at < datetime.utcnow():
        return False


    # Mark OTP as used
    record.is_used = True
    db.session.commit()

    return True



def delete_expired_otps():
    """
    Remove expired OTP records
    """

    expired_records = OtpLog.query.filter(
        OtpLog.expires_at < datetime.utcnow()
    ).all()


    for record in expired_records:
        db.session.delete(record)


    db.session.commit()

    return True

