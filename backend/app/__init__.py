from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.database import db
from app.api import api_bp
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
app.config['TESTING'] = os.getenv('TESTING', 'False') == 'True'

# Configure logging
import logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
# Use CORS_ORIGINS from .env
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
CORS(app, resources={r"/api/*": {"origins": cors_origins}})

app.register_blueprint(api_bp, url_prefix='/api')

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return False  # Placeholder for token revocation