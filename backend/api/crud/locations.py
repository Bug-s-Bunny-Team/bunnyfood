from typing import List, Optional

from sqlalchemy.orm import aliased

from api.crud import BaseCRUD
from db import models


class LocationsCRUD(BaseCRUD):
    def get_by_id(self, location_id: int) -> Optional[models.Location]:
        location = self._db.query(models.Location).filter_by(id=location_id).first()
        return location

    def get_from_filters(
        self,
        user: models.User,
        only_from_followed: bool = True,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        current_lat: Optional[float] = None,
        current_long: Optional[float] = None,
        radius: Optional[int] = None,
        min_rating: Optional[float] = None,
    ) -> List[models.Location]:
        stmt = self._db.query(
            models.Location,
            models.Location.distance(
                lat=current_lat if current_lat else 0,
                lng=current_long if current_long else 0,
            ).label('distance'),
        ).subquery()

        location_alias = aliased(models.Location, stmt)
        locations = self._db.query(location_alias)
        filter_radius = all([current_lat, current_long, radius])

        if min_rating:
            locations = locations.filter(stmt.c.score >= min_rating)
        if lat and long:
            locations = locations.filter(stmt.c.lat == lat, stmt.c.long == long)
        if only_from_followed:
            posts = (
                self._db.query(models.Post.id)
                .join(models.SocialProfile)
                .filter(
                    models.SocialProfile.id.in_(
                        [profile.id for profile in user.followed_profiles]
                    )
                )
                .subquery()
            )
            locations = locations.join(models.Post).filter(models.Post.id.in_(posts))
        if filter_radius:
            # filter by radius from current location
            # https://stackoverflow.com/questions/51014687/convert-a-complex-sql-query-to-sqlalchemy
            locations = locations.filter(stmt.c.distance <= radius).order_by(
                stmt.c.distance
            )

        if not filter_radius:
            locations = locations.order_by(stmt.c.score.desc())
        locations = locations.all()
        # locations = flatten_results(locations, 'distance')

        return locations
