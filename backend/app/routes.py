from flask import Blueprint, jsonify, request
from app.database import db
from app.models import User, Track

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Flask Racer X is running'})

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api_bp.route('/tracks', methods=['GET'])
def get_tracks():
    tracks = Track.query.all()
    return jsonify([track.to_dict() for track in tracks])

@api_bp.route('/races', methods=['POST'])
def create_track():
    data = request.get_json()
    track = Track(title=data['title'], artist=data.get('artist'), genre=data.get('genre'))
    db.session.add(track)
    db.session.commit()
    return jsonify(track.to_dict()), 201