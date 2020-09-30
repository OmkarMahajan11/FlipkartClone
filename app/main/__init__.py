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
    app.register_blueprint(user_blueprint, user_prefix="/user")
    app.register_blueprinnt(category_blueprint, user_prefix="/category")
    app.register_blueprinnt(product_blueprint, user_prefix="/product")
    
    return app