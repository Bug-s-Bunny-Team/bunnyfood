from sqlmodel import Session

from db import models


def populate_db(session: Session):
    profiles = [
        models.SocialProfile(id=1, username='testprofile1'),
        models.SocialProfile(id=2, username='testprofile2'),
        models.SocialProfile(id=3, username='testprofile3'),
    ]
    session.add_all(profiles)

    users = [
        models.User(id=2, username='testuser1'),
        models.User(id=3, username='testuser2'),
        models.User(id=4, username='testuser3'),
    ]
    session.add_all(users)

    locations = [
        models.Location(id=1, name='testlocation1', description='some desc', score=1),
        models.Location(id=2, name='testlocation2', description='some desc', score=1),
        models.Location(id=3, name='testlocation3', description='some desc', score=1),
        models.Location(id=4, name='testlocation4', description='some desc', score=4),
        models.Location(id=5, name='testlocation5', description='some desc', score=4),
        models.Location(
            id=6,
            name='testlocation6',
            description='some desc',
            score=4,
            lat=43.5,
            long=53.4,
        ),
    ]
    session.add_all(locations)

    user = models.User(id=1, username='testuser')
    user.followed_profiles.append(profiles[0])
    user.followed_profiles.append(profiles[2])
    session.add(user)

    posts = [
        models.Post(id=1, profile_id=1, location_id=4),
        models.Post(id=2, profile_id=1, location_id=5),
        models.Post(id=3, profile_id=2, location_id=4),
        models.Post(id=4, profile_id=2, location_id=5),
    ]
    session.add_all(posts)

    session.commit()
