from flask import Flask
from flask_login import LoginManager
from config import Config

login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config.from_object(config_class)
    login_manager.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)
    return app
