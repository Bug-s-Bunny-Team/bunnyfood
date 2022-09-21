import { get, Writable, writable } from 'svelte/store';
import { Filter, Location, Position } from '../../models'
import Locations from '../../../mock/locations.json'

export class ResultsModel {
    private static resultsModelInstance : ResultsModel = ResultsModel.construct_session();

    private static construct_session() : ResultsModel {
        return new ResultsModel();
    }

    static getInstance() : ResultsModel {
        return this.resultsModelInstance;
    }

    private constructor() { 
    }

    #rankedList: Writable<Location[]> = writable();
   
    get rankedList() { return this.#rankedList }
    
    async getRankedList(filter: Filter) : Promise<Location[]> {
        this.#rankedList.set(this.fixLocations(Locations));
        return get(this.#rankedList);
    }

    fixLocations(list: any[]) : Location[] {
        return list.map(location => {return new Location(location.id, location.name, new Position(location.lat, location.long), location.address, location.maps_place_id, location.score)})
    }

    getById(id: number) : Location {
        return get(this.#rankedList).find(location => {return location.id == id});
    }
}
