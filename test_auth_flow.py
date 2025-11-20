import sys
import os
import time

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app
from extensions import db
from models.user import User
from models.otp_log import OtpLog
from services.auth_service import hash_password

app = create_app()

def test_registration_flow():
    with app.app_context():
        email = "test_farmer@example.com"
        phone = "+919876543210"
        
        # Cleanup previous test run
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            OtpLog.query.filter_by(user_id=existing_user.id).delete()
            db.session.delete(existing_user)
            db.session.commit()
            print("Cleaned up previous test user.")

        # Step 1: Simulate Registration Request (Send OTP)
        print("Step 1: Creating user and sending OTP...")
        user = User(
            name="Test Farmer",
            email=email,
            phone=phone,
            role="FARMER",
            password_hash=hash_password("password123"),
            is_active=True,
            is_approved=False
        )
        db.session.add(user)
        db.session.commit()
        
        # Create OTP
        from services.otp_service import create_sms_otp_for_user
        create_sms_otp_for_user(user.id)
        
        # Verify OTP Log exists
        otp_log = OtpLog.query.filter_by(user_id=user.id, is_used=False).first()
        if not otp_log:
            print("FAILED: OTP Log not created.")
            return
        
        print(f"OTP Generated: {otp_log.otp_code}")
        
        # Step 2: Simulate OTP Verification
        print("Step 2: Verifying OTP...")
        if otp_log.otp_code:
            otp_log.is_used = True
            user.is_approved = True
            db.session.commit()
            
            updated_user = User.query.get(user.id)
            if updated_user.is_approved:
                print("SUCCESS: User approved after OTP verification.")
            else:
                print("FAILED: User not approved.")
        else:
            print("FAILED: No OTP code found.")

if __name__ == "__main__":
    test_registration_flow()
