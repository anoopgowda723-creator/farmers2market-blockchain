from flask import Flask
from config import DevelopmentConfig
from extensions import db
from routes import register_blueprints

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    register_blueprints(app)

    @app.route("/health")
    def health_check():
        return {"status": "ok", "message": "Farmer Market backend working"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
