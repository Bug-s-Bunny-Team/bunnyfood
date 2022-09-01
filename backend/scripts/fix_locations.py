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
        geocode_result = gmaps.geocode(l.name)
        if geocode_result:
            geocode_result = geocode_result[0]
            coords = geocode_result['geometry']['location']
            maps_place_id = geocode_result.get('place_id')

            place = gmaps.place(place_id=maps_place_id)
            address = place['result']['formatted_address']
            name = place['result']['name']

            print(f'{name} - {address} - {maps_place_id}')

            if session.query(models.Location).filter_by(maps_place_id=maps_place_id).first():
                print('location already existing, deleting')
                session.delete(l)
                session.commit()
            else:
                l.name = name
                l.lat = coords['lat']
                l.long = coords['lng']
                l.address = address
                l.maps_place_id = maps_place_id
                session.add(l)
                session.commit()
        else:
            print(f'No result for "{l.name}"')

    print('Cleaning up invalid locations')
    session.query(models.Location).filter(models.Location.maps_place_id == None).delete()
    session.commit()


if __name__ == '__main__':
    main()
