# backend/app.py

from flask import Flask
from config import DevelopmentConfig
from extensions import db
from routes import register_blueprints

# 🔹 NEW: LoginManager for authentication
from flask_login import LoginManager
from models.user import User


# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = "auth.login"   # redirect if not logged-in


def create_app(config_class=DevelopmentConfig):
    # Create Flask app with template + static folders
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    # Initialize extensions
    db.init_app(app)

    # Initialize login manager
    login_manager.init_app(app)

    # Initialize blockchain service
    from services.blockchain_service import blockchain_service
    blockchain_service.init_app(app)
    
    # Initialize payment service
    from services.payment_service import payment_service
    payment_service.init_app(app)

    # User session loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register all blueprints
    register_blueprints(app)

    # Simple health check route
    @app.route("/health")
    def health_check():
        return {"status": "ok", "message": "Farmer Market backend working"}

    return app


# Run server
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
