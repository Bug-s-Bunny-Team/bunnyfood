import { Info, RequestError } from '../../models'
import Infos from '../../../mock/info.json'

export class LocationModel {
    private static locationModelInstance : LocationModel = LocationModel.construct_session();

    private static construct_session() : LocationModel {
        return new LocationModel();
    }

    static getInstance() : LocationModel {
        return this.locationModelInstance;
    }

    private constructor() { 
    }
        
    getInfo = jest.fn(async function(id: number, parentNode: HTMLElement) : Promise<Info> {
        let info: Info = Infos.find(info => info.id==id);
        if(info) return new Info(info.name, info.img, info.address, info.score, info.phone_number, info.types, info.website);
        else throw new RequestError(404, "Error with request to G_API");
    });
}
