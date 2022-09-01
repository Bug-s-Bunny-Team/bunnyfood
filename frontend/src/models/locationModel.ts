import { Info, Location, RequestError } from '../models'
import { ResultsModel } from './resultsModel';

export class LocationModel {
    private static locationModelInstance : LocationModel = LocationModel.construct_session();

    private static construct_session() : LocationModel {
        let result = new LocationModel();
        return result;
    }

    static getInstance() : LocationModel {
        return this.locationModelInstance;
    }

    private constructor() { 
    }
        
    async getInfo(id: number, parentNode: HTMLElement) : Promise<Info> {
        const location: Location = ResultsModel.getInstance().getById(id);
        const attribution_div = document.createElement('div');
        parentNode.append(attribution_div);

        // google will be defined once the application runs
        let service = new google.maps.places.PlacesService(attribution_div);
        let fields = ['photos', 'international_phone_number'];

        
        return new Promise((resolve) => {
            service.getDetails({placeId: location.maps_place_id, fields: fields}, 
                function(result, status) {
                        if (status === google.maps.places.PlacesServiceStatus.OK) {
                            resolve(new Info(location.name, 
                                             result.photos && result.photos[0] ? 
                                                    {height: result.photos[0].height, 
                                                     width: result.photos[0].width, 
                                                     url: result.photos[0].getUrl(), 
                                                     alt: ""}
                                                :   {height: 20, 
                                                     width: 400,
                                                     url: "",
                                                     alt: "image unavailable"}, 
                                             location.address,
                                             location.score,
                                             result.international_phone_number));
                        } else {
                            throw new RequestError(status, "Error with request to G_API");
                        }
                });
        });
    }
}
