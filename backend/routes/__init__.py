# routes/__init__.py

# Import blueprints
from .main_routes import main_bp
from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .farmer_routes import farmer_bp
from .buyer_routes import buyer_bp
from .delivery_routes import delivery_bp
from .payment_routes import payment_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(farmer_bp, url_prefix="/farmer")
    app.register_blueprint(buyer_bp, url_prefix="/buyer")
    app.register_blueprint(delivery_bp, url_prefix="/delivery")
    app.register_blueprint(payment_bp, url_prefix="/payment")