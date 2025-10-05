from flask import Blueprint, jsonify, request
from app.database import db
from app.models import User

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Flask Racer X is running'})

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])