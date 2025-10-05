from flask import Flask
from flask_cors import CORS
from app.database import db, migrate
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    from backend.app.routes.users_routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app