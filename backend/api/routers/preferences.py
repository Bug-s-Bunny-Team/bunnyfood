from fastapi import APIRouter

from api import schemas
from api.schemas import GuideType

router = APIRouter()


@router.get(
    '/preferences',
    response_model=schemas.UserPreferences,
    response_model_exclude_unset=True,
)
def get_user_prefs():
    
    return schemas.UserPreferences(default_guide_view=GuideType.LIST)
