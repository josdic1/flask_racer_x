from flask import Blueprint, jsonify, request
from app.database import db
from app.models import User, Track, Track_Link

tracks_bp = Blueprint('track_bp', __name__) 

@tracks_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Flask Racer X is running'})

@tracks_bp.route('/tracks', methods=['GET'])
def get_tracks():
    tracks = Track.query.all()
    return jsonify([track.to_dict() for track in tracks])

@tracks_bp.route('/tracks/<int:id>', methods=['GET'])
def get_track(id):
    track = Track.query.get_or_404(id)
    return jsonify(track.to_dict())

@tracks_bp.route('/tracks', methods=['POST'])
def create_track():
    data = request.get_json()
    track = Track(title=data['title'], artist=data.get('artist'), genre=data.get('genre'))
    db.session.add(track)
    db.session.commit()
    return jsonify(track.to_dict()), 201

@tracks_bp.route('/tracks/<int:id>', methods=['DELETE'])
def delete_track(id):
    track = Track.query.get_or_404(id)
    db.session.delete(track)
    db.session.commit()
    return jsonify({'message': 'Track deleted'}), 200

@tracks_bp.route('/tracks/<int:id>', methods=['PUT', 'PATCH'])
def update_track(id):
    track = Track.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        track.title = data['title']
    if 'artist' in data:
        track.artist = data['artist']
    if 'genre' in data:
        track.genre = data['genre']
    
    db.session.commit()
    return jsonify(track.to_dict()), 200

@tracks_bp.route('/tracks/<int:track_id>/links', methods=['GET'])
def get_links_for_track(track_id):
    track = Track.query.get_or_404(track_id)
    links = Track_Link.query.filter_by(track_id=track.id).all()
    return jsonify([link.to_dict() for link in links])  

@tracks_bp.route('/tracks/<int:track_id>/links', methods=['POST'])
def add_link_to_track(track_id):
    track = Track.query.get_or_404(track_id)
    data = request.get_json()
    link = Track_Link(link_type=data['link_type'], link_url=data['link_url'], track_id=track.id)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), 201

@tracks_bp.route('/tracks/<int:track_id>/links/<int:link_id>', methods=['DELETE'])
def delete_link_from_track(track_id, link_id):
    track = Track.query.get_or_404(track_id)
    link = Track_Link.query.filter_by(id=link_id, track_id=track.id).first_or_404()
    db.session.delete(link)
    db.session.commit()
    return jsonify({'message': 'Link deleted'}), 200

@tracks_bp.route('/tracks/<int:track_id>/links/<int:link_id>', methods=['PUT', 'PATCH'])
def update_link_for_track(track_id, link_id):
    track = Track.query.get_or_404(track_id)
    link = Track_Link.query.filter_by(id=link_id, track_id=track.id).first_or_404()
    data = request.get_json()
    
    if 'link_type' in data:
        link.link_type = data['link_type']
    if 'link_url' in data:
        link.link_url = data['link_url']
    
    db.session.commit()
    return jsonify(link.to_dict()), 200

@tracks_bp.route('/tracks/search', methods=['GET'])
def search_tracks():
    title = request.args.get('title')
    artist = request.args.get('artist')
    genre = request.args.get('genre')
    
    query = Track.query
    if title:
        query = query.filter(Track.title.ilike(f'%{title}%'))
    if artist:
        query = query.filter(Track.artist.ilike(f'%{artist}%'))
    if genre:
        query = query.filter(Track.genre.ilike(f'%{genre}%'))
    
    tracks = query.all()
    return jsonify([track.to_dict() for track in tracks])


