from flask import Blueprint, jsonify, request
from app.database import db
from app.models import User, TokenBlocklist
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    unset_jwt_cookies,
)
from datetime import timedelta

api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Flask Racer X is running'})


@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=30))
    refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=14))
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


@api_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, expires_delta=timedelta(minutes=30))
    return jsonify({'access_token': access_token}), 200


@api_bp.route('/logout', methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt().get('jti')
    if jti:
        # add to blocklist
        tb = TokenBlocklist(jti=jti)
        db.session.add(tb)
        db.session.commit()
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])