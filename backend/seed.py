from app import create_app
from app.models import User, Track, TrackLink
from datetime import datetime, timezone
from app.database import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()


    user1 = User(name="Josh", password=bcrypt.generate_password_hash("pass1").decode("utf-8"))
    user2 = User(name="Dorrie", password=bcrypt.generate_password_hash("pass2").decode("utf-8"))

    db.session.add_all([user1, user2])
    db.session.commit() 

    track1 = Track(track="Whoa Ghana", artist="Beautiful's Dream", genre="multi", user_id=user1.id)
    track2 = Track(track="No Hitting", artist="Beautiful's Dream", genre="multi", user_id=user1.id)
    track3 = Track(track="Donut City", artist="Beautiful's Dream", genre="multi", user_id=user1.id)
    track4 = Track(track="Can I Get an Intro", artist="Beautiful's Dream", genre="multi", user_id=user1.id)
    track5 = Track(track="Dorrie's Dumpling", artist="Dorrance", genre="demo", user_id=user2.id)

    db.session.add_all([track1, track2, track3, track4, track5])
    db.session.commit() 


    track_link1 = TrackLink(link_type="youtube", link_url="https://www.youtube.com/watch?v=OKgmt14oonA", track=track1) 
    track_link2 = TrackLink(link_type="youtube", link_url="https://www.youtube.com/watch?v=0MzQ2Pg4Zkc", track=track2) 
    track_link3 = TrackLink(link_type="spotify", link_url="https://open.spotify.com/track/0t4UVXTeUEtFCcMZGjsHPH?si=6e6be9b85c69428a", track=track1) 
    track_link4 = TrackLink(link_type="spotify", link_url="https://open.spotify.com/track/3HZ7gHamJJzcjKbEENuGyY?si=518cc1dba71443c4", track=track3) 

    db.session.add_all([track_link1, track_link2, track_link3, track_link4])
    db.session.commit()

    print("✅ Database seeded with users, tracks, and track links (with hashed passwords)!")