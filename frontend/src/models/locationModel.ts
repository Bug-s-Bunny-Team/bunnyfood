import { Info, Location, RequestError } from '../models'
import { ResultsModel } from './resultsModel';

export class LocationModel {
    private static resultsModelInstance : LocationModel = LocationModel.construct_session();

    private static construct_session() : LocationModel {
        let result = new LocationModel();
        return result;
    }

    static getInstance() : LocationModel {
        return this.resultsModelInstance;
    }

    private constructor() { 
    }

    private static static_delay_ms = 200;
    
    async getInfo(id: number, parentNode: HTMLElement) : Promise<Info> {
        await new Promise(r => setTimeout(r, LocationModel.static_delay_ms));
        const location: Location = ResultsModel.getInstance().getById(id);
        const attribution_div = document.createElement('div');
        parentNode.append(attribution_div);

        let latlng = new google.maps.LatLng(location.position.lat, location.position.long);
        let service = new google.maps.places.PlacesService(attribution_div);
        let fields = ['place_id', 'name', 'formatted_address', 'photos'];

        
        return new Promise((resolve) => {
            service.findPlaceFromQuery({query: location.name, fields: fields, locationBias: latlng}, 
                function(results, status) {
                        if (status === google.maps.places.PlacesServiceStatus.OK) {
                            resolve(new Info(results[0].name, 
                                            {height: results[0].photos[0].height, width:results[0].photos[0].width, url: results[0].photos[0].getUrl()}, 
                                            results[0].formatted_address,
                                            location.score));
                        } else {
                            throw new RequestError(400, "Error with request to G_API");
                        }
                });
        });
    }
}
