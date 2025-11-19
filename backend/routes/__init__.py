from .main_routes import main_bp
from .auth_routes import auth_bp
# Later we’ll also import others:
# from .farmer_routes import farmer_bp
# from .buyer_routes import buyer_bp
# from .delivery_routes import delivery_bp
# from .admin_routes import admin_bp
# from .payment_routes import payment_bp
# from .blockchain_routes import blockchain_bp


from .auth_routes import auth_bp
from .main_routes import main_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")


    # Later:
    # app.register_blueprint(farmer_bp, url_prefix="/farmer")
    # app.register_blueprint(buyer_bp, url_prefix="/buyer")
    # app.register_blueprint(delivery_bp, url_prefix="/delivery")
    # app.register_blueprint(admin_bp, url_prefix="/admin")
    # app.register_blueprint(payment_bp, url_prefix="/payment")
    # app.register_blueprint(blockchain_bp, url_prefix="/blockchain")
