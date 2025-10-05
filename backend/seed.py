from app import create_app
from app.models import User, Track, Track_Link
from app.database import db

app = create_app()

with app.app_context():
    # Drop and recreate tables for a clean dev seed
    db.drop_all()
    db.create_all()

    # Create users
    user1 = User(username="josh", email="josh@example.com")
    user1.set_password("pass1")
    user2 = User(username="dorrie", email="dorrie@example.com")
    user2.set_password("pass2")

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create tracks (use 'title' field)
    track1 = Track(title="Whoa Ghana", artist="Beautiful's Dream", genre="multi", user_id=user1.id)
    track2 = Track(title="No Hitting", artist="Beautiful's Dream", genre="multi", user_id=user1.id)
    track3 = Track(title="Donut City", artist="Beautiful's Dream", genre="multi", user_id=user1.id)
    track4 = Track(title="Can I Get an Intro", artist="Beautiful's Dream", genre="multi", user_id=user1.id)
    track5 = Track(title="Dorrie's Dumpling", artist="Dorrance", genre="demo", user_id=user2.id)

    db.session.add_all([track1, track2, track3, track4, track5])
    db.session.commit()

    # Create track links using Track_Link model and associate with user who owns the track
    tl1 = Track_Link(link_type="youtube", link_url="https://www.youtube.com/watch?v=OKgmt14oonA", track_id=track1.id, user_id=user1.id)
    tl2 = Track_Link(link_type="youtube", link_url="https://www.youtube.com/watch?v=0MzQ2Pg4Zkc", track_id=track2.id, user_id=user1.id)
    tl3 = Track_Link(link_type="spotify", link_url="https://open.spotify.com/track/0t4UVXTeUEtFCcMZGjsHPH?si=6e6be9b85c69428a", track_id=track1.id, user_id=user1.id)
    tl4 = Track_Link(link_type="spotify", link_url="https://open.spotify.com/track/3HZ7gHamJJzcjKbEENuGyY?si=518cc1dba71443c4", track_id=track3.id, user_id=user1.id)

    db.session.add_all([tl1, tl2, tl3, tl4])
    db.session.commit()

    print("✅ Database seeded with users, tracks, and track links (with hashed passwords)!")