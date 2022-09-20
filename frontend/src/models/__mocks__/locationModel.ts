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
        
    async getInfo(id: number, parentNode: HTMLElement) : Promise<Info> {
        let _info: Info = null;
        (Infos as any[]).forEach(info => {
            if(info.id == id) {
                _info = new Info(info.name, info.img, info.address, info.score, info.phone_number, info.types, info.website);
            }
        });
        if(_info) return _info;
        else throw new RequestError(404, "Error with request to G_API");
    }
}
