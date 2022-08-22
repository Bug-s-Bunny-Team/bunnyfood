import math

from sqlalchemy.orm import Session


def get_or_create(db: Session, model, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance


def gc_distance(lat1, lng1, lat2, lng2, math_lib=None):
    """
    Calculate distance between two coordinates.
    https://en.wikipedia.org/wiki/Great-circle_distance
    """
    if not math_lib:
        math_lib = math

    ang = math_lib.acos(
        math_lib.cos(math_lib.radians(lat1))
        * math_lib.cos(math_lib.radians(lat2))
        * math_lib.cos(math_lib.radians(lng2) - math_lib.radians(lng1))
        + math_lib.sin(math_lib.radians(lat1)) * math_lib.sin(math_lib.radians(lat2))
    )

    # return 6371 * ang   # distance in kilometers
    return 6371000 * ang    # distance in meters
