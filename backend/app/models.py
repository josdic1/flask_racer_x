from app.database import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    tracks = db.Column('Track', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Track(db.Model):
    __tablename__ = 'tracks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tracks', lazy=True))
    links = db.relationship('Track_Link', backref='track', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist or '',
            'genre': self.genre or '',
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'links': [link.to_dict() for link in self.links]
        }

class Track_Link(db.Model):
    __tablename__ = 'track_links'
    
    id = db.Column(db.Integer, primary_key=True)
    link_type = db.Column(db.String(50), nullable=False)
    link_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), nullable=False)
    track = db.relationship('Track', backref=db.backref('links', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    user = db.relationship('User', backref=db.backref('track_links', lazy=True))  
    
    def to_dict(self):
        return {
            'id': self.id,
            'link_type': self.link_type,
            'link_url': self.link_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'track_id': self.track_id,
            'user_id': self.user_id  # Added
        }