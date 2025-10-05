from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models import Track, Track_Link
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.pagination import paginate_query  # Import pagination utility

tracks_bp = Blueprint('track_bp', __name__)

@tracks_bp.route('/health', methods=['GET'])
def health():
    """Return API health status."""
    return jsonify({'status': 'healthy', 'message': 'Flask Racer X is running'}), 200

@tracks_bp.route('/tracks', methods=['GET'])
def get_tracks():
    """Retrieve paginated list of all tracks."""
    query = Track.query
    return jsonify(paginate_query(query)), 200

@tracks_bp.route('/tracks/<int:id>', methods=['GET'])
def get_track(id):
    """Retrieve a track by ID."""
    track = Track.query.get_or_404(id)
    return jsonify(track.to_dict()), 200

@tracks_bp.route('/tracks', methods=['POST'])
@jwt_required()
def create_track():
    """Create a new track.
    Request Body: { "title": str, "artist": str (optional), "genre": str (optional) }
    Returns: JSON of created track (201)
    """
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")

    required_fields = ['title']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required field: title")

    if not isinstance(data['title'], str) or not data['title'].strip():
        abort(400, description="title must be a non-empty string")
    if 'artist' in data and not isinstance(data['artist'], (str, type(None))):
        abort(400, description="artist must be a string or null")
    if 'genre' in data and not isinstance(data['genre'], (str, type(None))):
        abort(400, description="genre must be a string or null")

    try:
        # If authenticated, associate the track with the requesting user
        user_id = None
        try:
            user_id = get_jwt_identity()
        except Exception:
            user_id = None

        track = Track(
            title=data['title'],
            artist=data.get('artist'),
            genre=data.get('genre'),
            user_id=user_id if user_id is not None else data.get('user_id', None)
        )
        db.session.add(track)
        db.session.commit()
        return jsonify(track.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Duplicate track or invalid data")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")

@tracks_bp.route('/tracks/<int:id>', methods=['DELETE'])
def delete_track(id):
    """Delete a track by ID."""
    track = Track.query.get_or_404(id)
    try:
        data = track.to_dict()  # Capture data before deletion
        db.session.delete(track)
        db.session.commit()
        return jsonify({'message': 'Track deleted', 'data': data}), 200
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")

@tracks_bp.route('/tracks/<int:id>', methods=['PUT', 'PATCH'])
def update_track(id):
    """Update a track by ID.
    Request Body: { "title": str (optional), "artist": str (optional), "genre": str (optional) }
    Returns: JSON of updated track (200)
    """
    track = Track.query.get_or_404(id)
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")

    if 'title' in data:
        if not isinstance(data['title'], str) or not data['title'].strip():
            abort(400, description="title must be a non-empty string")
        track.title = data['title']
    if 'artist' in data:
        if not isinstance(data['artist'], (str, type(None))):
            abort(400, description="artist must be a string or null")
        track.artist = data['artist']
    if 'genre' in data:
        if not isinstance(data['genre'], (str, type(None))):
            abort(400, description="genre must be a string or null")
        track.genre = data['genre']

    try:
        db.session.commit()
        return jsonify(track.to_dict()), 200
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Duplicate track or invalid data")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")

@tracks_bp.route('/tracks/<int:track_id>/links', methods=['GET'])
def get_links_for_track(track_id):
    """Retrieve paginated list of links for a specific track."""
    Track.query.get_or_404(track_id)  # Validate track exists
    query = Track_Link.query.filter_by(track_id=track_id)
    return jsonify(paginate_query(query)), 200

@tracks_bp.route('/tracks/<int:track_id>/links', methods=['POST'])
@jwt_required()
def add_link_to_track(track_id):
    """Add a link to a track.
    Request Body: { "link_type": str, "link_url": str }
    Returns: JSON of created track link (201)
    """
    Track.query.get_or_404(track_id)  # Validate track exists
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")

    required_fields = ['link_type', 'link_url']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields: link_type, link_url")

    if not isinstance(data['link_type'], str) or not data['link_type'].strip():
        abort(400, description="link_type must be a non-empty string")
    if not isinstance(data['link_url'], str) or not data['link_url'].strip():
        abort(400, description="link_url must be a non-empty string")

    try:
        # user_id from token if available
        user_id = None
        try:
            user_id = get_jwt_identity()
        except Exception:
            user_id = None

        link = Track_Link(
            link_type=data['link_type'],
            link_url=data['link_url'],
            track_id=track_id,
            user_id=user_id if user_id is not None else data.get('user_id', None)
        )
        db.session.add(link)
        db.session.commit()
        return jsonify(link.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Duplicate link or invalid track_id")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")

@tracks_bp.route('/tracks/<int:track_id>/links/<int:link_id>', methods=['DELETE'])
def delete_link_from_track(track_id, link_id):
    """Delete a track link by ID for a specific track."""
    Track.query.get_or_404(track_id)  # Validate track exists
    link = Track_Link.query.filter_by(id=link_id, track_id=track_id).first_or_404()
    try:
        data = link.to_dict()  # Capture data before deletion
        db.session.delete(link)
        db.session.commit()
        return jsonify({'message': 'Link deleted', 'data': data}), 200
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")

@tracks_bp.route('/tracks/<int:track_id>/links/<int:link_id>', methods=['PUT', 'PATCH'])
def update_link_for_track(track_id, link_id):
    """Update a track link by ID for a specific track.
    Request Body: { "link_type": str (optional), "link_url": str (optional) }
    Returns: JSON of updated track link (200)
    """
    Track.query.get_or_404(track_id)  # Validate track exists
    link = Track_Link.query.filter_by(id=link_id, track_id=track_id).first_or_404()
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")

    if 'link_type' in data:
        if not isinstance(data['link_type'], str) or not data['link_type'].strip():
            abort(400, description="link_type must be a non-empty string")
        link.link_type = data['link_type']
    if 'link_url' in data:
        if not isinstance(data['link_url'], str) or not data['link_url'].strip():
            abort(400, description="link_url must be a non-empty string")
        link.link_url = data['link_url']

    try:
        db.session.commit()
        return jsonify(link.to_dict()), 200
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Duplicate link or invalid data")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")

@tracks_bp.route('/tracks/search', methods=['GET'])
def search_tracks():
    """Search tracks by title, artist, or genre.
    Query Params: title (str, optional), artist (str, optional), genre (str, optional)
    Returns: Paginated list of matching tracks
    """
    title = request.args.get('title', '').strip()
    artist = request.args.get('artist', '').strip()
    genre = request.args.get('genre', '').strip()

    if len(title) > 100 or len(artist) > 100 or len(genre) > 100:
        abort(400, description="Query parameters cannot exceed 100 characters")

    query = Track.query
    if title:
        query = query.filter(Track.title.ilike(f'%{title}%'))
    if artist:
        query = query.filter(Track.artist.ilike(f'%{artist}%'))
    if genre:
        query = query.filter(Track.genre.ilike(f'%{genre}%'))

    return jsonify(paginate_query(query)), 200