from app import create_app
from extensions import db
from models.user import User
from services.auth_service import hash_password

app = create_app()

with app.app_context():

    email = "admin@farmer2market.com"

    existing = User.query.filter_by(email=email).first()

    if existing:
        print("===================================")
        print("ADMIN ALREADY EXISTS")
        print("Email :", existing.email)
        print("Role  :", existing.role)
        print("===================================")

    else:
        admin = User(
            name="ANOOP ADMIN",
            email=email,
            phone="9353645468",
            role="ADMIN",
            password_hash=hash_password("Admin@12345"),
            is_active=True,
            is_approved=True
        )

        db.session.add(admin)
        db.session.commit()

        print("===================================")
        print("ADMIN CREATED SUCCESSFULLY")
        print("Email :", email)
        print("Password : Admin@12345")
        print("===================================")