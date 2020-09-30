from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from ..config import app_config
from .routes import user as user_blueprint
from .routes import category as category_blueprint
from .routes import product as product_blueprint

def create_app(env):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[env])
    app.config.from_pyfile("config.py")
    db.init_app(app)
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(category_blueprint, url_prefix="/category")
    app.register_blueprint(product_blueprint, url_prefix="/product")
    
    return app