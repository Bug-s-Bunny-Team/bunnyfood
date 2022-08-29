import { get, Writable, writable } from 'svelte/store';
import { Filter, Location, Position } from '../../models'
import locations from '../../../mock/locations.json'

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

    rankedList: Writable<Location[]> = writable();
    
    async getRankedList(filter: Filter) : Promise<Location[]> {
        this.rankedList.set(this.fixLocations(locations));
        return get(this.rankedList);
    }

    fixLocations(list: any[]) : Location[] {
        return list.map(location => {return new Location(location.id, location.name, new Position(location.lat, location.long), location.score)})
    }

    getById(id: number) : Location {
        return get(this.rankedList).find(location => {return location.id == id});
    }
}
