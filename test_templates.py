import sys
import os
import traceback
from flask_login import login_user

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app
from extensions import db
from models.user import User

app = create_app()

import uuid

# ... imports ...

def test_templates():
    with app.test_client() as client:
        with app.app_context():
            unique_id = str(uuid.uuid4())[:8]
            email = f"test_{unique_id}@test.com"
            phone = str(uuid.uuid4().int)[:10]
            
            try:
                farmer = User(
                    name="Test Farmer", 
                    email=email, 
                    phone=phone,
                    password_hash="dummyhash",
                    role="FARMER", 
                    is_active=True, 
                    is_approved=True
                )
                db.session.add(farmer)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"DB Error during setup: {e}")
                return

            # Login
            with client.session_transaction() as sess:
                sess['_user_id'] = str(farmer.id)
                sess['_fresh'] = True

            # Test Profile Page
            print("Testing Profile Page Rendering...")
            try:
                resp = client.get("/farmer/profile")
                if resp.status_code == 200:
                    print("PASS: Profile page rendered successfully.")
                else:
                    print(f"FAIL: Profile page returned {resp.status_code}")
                    print(resp.data.decode('utf-8')[:500])
            except Exception as e:
                print(f"FAIL: Exception during profile render: {e}")
                traceback.print_exc()

            # Test Product Create Page
            print("Testing Product Create Page Rendering...")
            try:
                resp = client.get("/farmer/products/new")
                if resp.status_code == 200:
                    print("PASS: Product Create page rendered successfully.")
                else:
                    print(f"FAIL: Product Create page returned {resp.status_code}")
                    print(resp.data.decode('utf-8')[:500])
            except Exception as e:
                print(f"FAIL: Exception during product create render: {e}")
                traceback.print_exc()

if __name__ == "__main__":
    test_templates()
