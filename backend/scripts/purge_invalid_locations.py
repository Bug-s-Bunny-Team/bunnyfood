import os

import googlemaps

from db import get_session, models

# change to 'prod' to run in production db
ENV = 'dev'


def main():
    gmaps = googlemaps.Client(key=os.environ['MAPS_API_KEY'])
    session = get_session(force_env=ENV)

    locations = session.query(models.Location).all()
    print(f'Got {len(locations)} locations from db')

    for l in locations:
        if l.maps_place_id:
            place = gmaps.place(place_id=l.maps_place_id)
            types = place['result']['types']
            if not 'food' in types:
                print(f'Deleting {l.name}')
                session.delete(l)
                session.commit()


if __name__ == '__main__':
    main()
