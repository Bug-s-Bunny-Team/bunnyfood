import { google_ready } from '../store';
import { Info, Location } from '../models'
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

    ready: boolean;

    private constructor() { 
        google_ready.subscribe(_ready => {this.ready = _ready})
    }

    private static static_delay_ms = 200;
    
    async getInfo(id: number) : Promise<Info> {
        if(this.ready) {
            await new Promise(r => setTimeout(r, LocationModel.static_delay_ms));
            const location: Location = ResultsModel.getInstance().getById(id);

            let latlng = new google.maps.LatLng(location.position.lat, location.position.long);
            let service = new google.maps.places.PlacesService(document.createElement('div'));
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
                                throw new Error("Error with request to G_API");
                            }
                    });
            });
        } else {
            throw new Error("google api not ready yet");
        }
    }
}
