from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from ..config import app_config

def create_app(env):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[env])
    app.config.from_pyfile("config.py")
    db.init_app(app)



    
    return app