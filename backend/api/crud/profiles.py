from typing import List, Optional

from sqlalchemy import column, func

from api import schemas
from api.crud import BaseCRUD
from api.utils import flatten_results
from db import models
from db.models import profiles_users_association
from db.utils import get_or_create


class ProfilesCRUD(BaseCRUD):
    def get_all(self) -> List[models.SocialProfile]:
        return self._db.query(models.SocialProfile).all()

    def get_by_id(self, profile_id: int):
        profile = self._db.query(models.SocialProfile).filter_by(id=profile_id).first()
        return profile

    def get_by_username(self, profile_username: str) -> Optional[models.SocialProfile]:
        profile = (
            self._db.query(models.SocialProfile)
            .filter_by(username=profile_username)
            .first()
        )
        return profile

    def get_most_popular(self, limit: int) -> List[models.SocialProfile]:
        profiles = (
            self._db.query(
                models.SocialProfile,
                func.count(profiles_users_association.c.right_id).label(
                    'followers_count'
                ),
            )
            .join(profiles_users_association)
            .group_by(models.SocialProfile)
            .order_by(column('followers_count').desc())
            .limit(limit)
            .all()
        )

        profiles = flatten_results(profiles, 'followers_count')

        return profiles

    def follow_profile(self, profile: schemas.FollowedSocialProfile, user: models.User):
        db_profile = get_or_create(
            self._db, models.SocialProfile, username=profile.username
        )
        user.followed_profiles.append(db_profile)
        self._db.add(user)
        self._db.commit()

    def unfollow_profile(self, profile: models.SocialProfile, user: models.User):
        user.followed_profiles.remove(profile)
        self._db.add(user)
        self._db.commit()

    def create_profile(self, profile_username: str) -> models.SocialProfile:
        profile = models.SocialProfile(username=profile_username)
        self._db.add(profile)
        self._db.commit()
        self._db.refresh(profile)
        return profile
