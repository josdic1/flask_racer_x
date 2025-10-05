from app import create_app
from app.database import db
from app.models import User, Track, TrackLink

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ app.db reset with fresh tables!")