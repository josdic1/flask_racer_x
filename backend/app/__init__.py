from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.database import db
import os
from dotenv import load_dotenv

load_dotenv()

# Create extensions instances that will be initialized in the factory
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(test_config=None):
    """Application factory to create and configure the Flask app.

    Using a factory avoids circular imports when modules import `app` at
    import-time (e.g. blueprints importing models which import database).
    """
    app = Flask(__name__)

    # Load configuration from environment or test_config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600'))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
    app.config['TESTING'] = os.getenv('TESTING', 'False') == 'True'

    if test_config:
        app.config.update(test_config)

    # Configure logging
    import logging
    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Configure CORS
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    # Import and register blueprints inside the factory to avoid circular imports
    from app.api import api_bp
    from app.routes.tracks_route import tracks_bp
    from app.routes.track_links_routes import track_links_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(tracks_bp, url_prefix='/api')
    app.register_blueprint(track_links_bp, url_prefix='/api')

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        # Check blocklist table for revoked tokens
        from app.models import TokenBlocklist
        jti = jwt_payload.get('jti')
        if jti is None:
            return False
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    return app