import { Info } from '../models'

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
    
    async getInfo(name: string) : Promise<Info> {
        await new Promise(r => setTimeout(r, LocationModel.static_delay_ms))
        return new Info(name, '', '347235618', 'piazza dei signori, 6');
        /*const response = await fetch(`dev-api/location/${name}`);
        return await response.json();*/
    }
}
