from typing import List

from fastapi import APIRouter

from api.schemas import Location

router = APIRouter()


@router.get(
    '/locations', response_model=List[Location], response_model_exclude_unset=True
)
def get_locations():
    return [
        Location(
            id=1,
            name='Panineria veneta',
            description='Una panineria random',
            score=5.0,
            lat=55.7535579,
            long=37.6187217,
        ),
        Location(
            id=2,
            name='Panineria veneta 2',
            description='Una panineria random 2',
            score=4.0,
            lat=55.7535579,
            long=37.6187217,
        ),
    ]


@router.get(
    '/locations/{location_id}',
    response_model=Location,
    response_model_exclude_unset=True,
)
def get_location(location_id: int):
    location = Location(
        id=location_id,
        name='Panineria veneta',
        description='Una panineria random',
        score=4.5,
        lat=55.7535579,
        long=37.6187217,
    )
    return location
