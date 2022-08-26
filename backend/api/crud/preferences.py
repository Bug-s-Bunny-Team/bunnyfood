from api import schemas
from api.crud import BaseCRUD
from db import models
from db.utils import get_or_create


class PreferencesCRUD(BaseCRUD):
    def get_from_user(self, user: models.User) -> models.UserPreferences:
        return get_or_create(self._db, models.UserPreferences, user=user)

    def update(
        self, updated_prefs: schemas.UserPreferences, user: models.User
    ) -> models.UserPreferences:
        prefs = get_or_create(self._db, models.UserPreferences, user=user)
        prefs.default_guide_view = updated_prefs.default_guide_view
        self._db.add(prefs)
        self._db.commit()
        return prefs
