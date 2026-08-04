# ==========================================
# Farmer2Market Backend Application
# ==========================================

import os
from pathlib import Path

from dotenv import load_dotenv


# ==========================================
# Load Environment (.env)
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
    print(f"[INFO] Loaded environment from: {ENV_FILE}")
else:
    print("[WARN] .env file not found")


# ==========================================
# Flask Imports
# ==========================================

from flask import Flask

from config import DevelopmentConfig
from extensions import db

from routes import register_blueprints


# ==========================================
# Authentication
# ==========================================

from flask_login import LoginManager
from models.user import User


login_manager = LoginManager()

login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to continue"


# ==========================================
# Application Factory
# ==========================================

def create_app(config_class=DevelopmentConfig):

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )


    # Load Flask Config
    app.config.from_object(config_class)


    # ======================================
    # Database Initialization
    # ======================================

    db.init_app(app)


    # ======================================
    # Login Manager
    # ======================================

    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))


    # ======================================
    # Blockchain Initialization
    # ======================================

    try:

        from services.blockchain_service import blockchain_service

        blockchain_service.init_app(app)

    except Exception as e:

        print(
            "[ERROR] Blockchain initialization failed:",
            e
        )


    # ======================================
    # Payment Initialization
    # ======================================

    try:

        from services.payment_service import payment_service

        payment_service.init_app(app)

    except Exception as e:

        print(
            "[ERROR] Payment initialization failed:",
            e
        )


    # ======================================
    # Register Routes
    # ======================================

    register_blueprints(app)


    # ======================================
    # Health Check
    # ======================================

    @app.route("/health")
    def health():

        return {
            "status": "success",
            "message": "Farmer2Market Backend Running"
        }


    return app



# ==========================================
# Run Server
# ==========================================

if __name__ == "__main__":

    app = create_app()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )