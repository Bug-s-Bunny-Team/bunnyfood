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
        if(!location) return new Promise((res, rej) => rej(new RequestError(404, "Error with request to G_API")));

        const attribution_div = document.createElement('div');
        parentNode.append(attribution_div);

        // google will be defined once the application runs
        let service = new (window.google || google).maps.places.PlacesService(attribution_div);
        let fields = ['photos', 'international_phone_number', 'website', 'types'];
        
        return new Promise((resolve, reject) => {
            service.getDetails({placeId: location.maps_place_id, fields: fields}, 
                function(result, status) {
                        if (status === (window.google || google).maps.places.PlacesServiceStatus.OK) {
                            resolve(new Info(location.name, 
                                             result.photos && result.photos[0] && result.photos[0].getUrl() ? 
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
                                             result.international_phone_number,
                                             result.types,
                                             result.website));
                        } else {
                            reject(new RequestError(status, "Error with request to G_API"));
                        }
                });
        });
    }
}
