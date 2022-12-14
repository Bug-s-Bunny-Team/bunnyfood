from sqlalchemy.orm import Session

from db import models


def populate_db(session: Session):
    profiles = [
        models.SocialProfile(username='testprofile1'),
        models.SocialProfile(username='testprofile2'),
        models.SocialProfile(username='testprofile3'),
        models.SocialProfile(username='testprofile4'),
        models.SocialProfile(username='testprofile5'),
    ]
    session.add_all(profiles)

    user = models.User(username='testuser')
    user.followed_profiles.append(profiles[0])
    user.followed_profiles.append(profiles[2])
    session.add(user)

    user = models.User(username='testuser1')
    user.followed_profiles.append(profiles[3])
    user.followed_profiles.append(profiles[4])
    session.add(user)

    users = [
        models.User(username='testuser2'),
        models.User(username='testuser3'),
    ]
    session.add_all(users)

    locations = [
        models.Location(name='testlocation1', description='some desc', score=1),
        models.Location(name='testlocation2', description='some desc', score=1),
        models.Location(name='testlocation3', description='some desc', score=1),
        models.Location(
            name='testlocation4',
            description='some desc',
            score=4,
            lat=55.7255843,
            long=37.6243329,
        ),
        models.Location(
            name='testlocation5',
            description='some desc',
            score=4,
            lat=55.7252157,
            long=37.6277554,
        ),
        models.Location(
            name='testlocation6',
            description='some desc',
            score=4,
            lat=55.7251432,
            long=37.6273906,
        ),
    ]
    session.add_all(locations)

    posts = [
        models.Post(profile_id=1, location_id=4),
        models.Post(profile_id=1, location_id=5),
        models.Post(profile_id=2, location_id=4),
        models.Post(profile_id=2, location_id=5),
    ]
    session.add_all(posts)

    session.commit()
