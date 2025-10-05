from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models import Track, Track_Link
from app.utils import paginate_query  # Import the pagination utility

track_links_bp = Blueprint('track_links', __name__)

@track_links_bp.route('/health', methods=['GET'])
def health():
    """Return API health status."""
    return jsonify({'status': 'healthy', 'message': 'Flask Racer X is running'}), 200

@track_links_bp.route('/track_links', methods=['GET'])
def get_track_links():
    """Retrieve paginated list of all track links."""
    query = Track_Link.query
    return jsonify(paginate_query(query)), 200

@track_links_bp.route('/track_links/<int:track_id>', methods=['GET'])
def get_track_links_by_track(track_id):
    """Retrieve track links for a specific track ID."""
    query = Track_Link.query.filter_by(track_id=track_id)
    return jsonify(paginate_query(query)), 200

@track_links_bp.route('/track_links', methods=['POST'])
def create_track_link():
    """Create a new track link.
    Request Body: { "link_type": str, "link_url": str, "track_id": int (optional) }
    Returns: JSON of created track link (201)
    """
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
    if 'track_id' in data and not isinstance(data['track_id'], (int, type(None))):
        abort(400, description="track_id must be an integer or null")
    
    try:
        track_link = Track_Link(
            link_type=data['link_type'],
            link_url=data['link_url'],
            track_id=data.get('track_id')
        )
        db.session.add(track_link)
        db.session.commit()
        return jsonify(track_link.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Invalid track_id or duplicate entry")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")

@track_links_bp.route('/track_links/<int:id>', methods=['DELETE'])
def delete_track_link(id):
    """Delete a track link by ID."""
    track_link = Track_Link.query.get_or_404(id)
    try:
        data = track_link.to_dict()  # Capture data before deletion
        db.session.delete(track_link)
        db.session.commit()
        return jsonify({'message': 'Track link deleted', 'data': data}), 200
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")


@track_links_bp.route('/track_links/<int:id>', methods=['PUT', 'PATCH'])
def update_track_link(id):
    """Update a track link by ID."""
    track_link = Track_Link.query.get_or_404(id)
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")
    
    if 'link_type' in data:
        if not isinstance(data['link_type'], str) or not data['link_type'].strip():
            abort(400, description="link_type must be a non-empty string")
        track_link.link_type = data['link_type']
    if 'link_url' in data:
        if not isinstance(data['link_url'], str) or not data['link_url'].strip():
            abort(400, description="link_url must be a non-empty string")
        track_link.link_url = data['link_url']
    if 'track_id' in data:
        if data['track_id'] is not None:
            Track.query.get_or_404(data['track_id'], description="Track with this ID not found")
        
        if not isinstance(data['track_id'], (int, type(None))):
            abort(400, description="track_id must be an integer or null")
        track_link.track_id = data['track_id']
    
    try:
        db.session.commit()
        return jsonify(track_link.to_dict()), 200
    except IntegrityError: # This now serves as a fallback, not primary validation
        db.session.rollback()
        abort(400, description="Duplicate entry detected")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Server error: {str(e)}")

@track_links_bp.route('/track_links/search', methods=['GET'])
def search_track_links_route():
    """Search track links by link_type or link_url.
    Query Param: q (string, max length 100)
    Returns: Paginated list of matching track links
    """
    query_str = request.args.get('q', '').strip()
    if len(query_str) > 100:
        abort(400, description="Query too long")
    
    query = Track_Link.query.filter(
        (Track_Link.link_type.ilike(f'%{query_str}%')) |
        (Track_Link.link_url.ilike(f'%{query_str}%'))
    )
    return jsonify(paginate_query(query)), 200