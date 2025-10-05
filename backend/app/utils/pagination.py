from flask import request, abort
from sqlalchemy.orm import Query

def paginate_query(query: Query, max_per_page: int = 100) -> dict:
    """
    Paginates a SQLAlchemy query and returns a standardized response.

    Args:
        query (Query): SQLAlchemy query to paginate.
        max_per_page (int): Maximum items per page (default: 100).

    Returns:
        dict: Dictionary containing paginated data and metadata.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if per_page > max_per_page:
        abort(400, description=f"per_page cannot exceed {max_per_page}")

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'data': [item.to_dict() for item in pagination.items],
        'page': pagination.page,
        'total': pagination.total,
        'pages': pagination.pages
    }