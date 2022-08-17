from fastapi import APIRouter

router = APIRouter()


@router.get('/locations')
def get_locations():
    return [
        {'id': 1, 'name': 'Panineria veneta', 'description': 'Una panineria random'}
    ]


@router.get('/locations/{location_id}')
def get_location(location_id: int):
    return {
        'id': location_id,
        'name': 'Panineria veneta',
        'description': 'Una panineria random',
    }
