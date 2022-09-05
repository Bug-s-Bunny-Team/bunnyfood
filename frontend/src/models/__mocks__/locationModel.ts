import { Info } from '../../models'

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
        return  new Info("mocked name", {height: 1, width: 1, url: "mocked url", alt: ""}, "mocked address", 1, "2938476528193", ["bar", "restaurant"], "www.google.com");
    }
}
