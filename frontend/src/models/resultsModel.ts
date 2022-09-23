import { get, Writable, writable } from 'svelte/store';
import { Filter, Location, Position, RequestError } from '../models'
import { RequestOptions } from './requestOptions';

export class ResultsModel {
    private static resultsModelInstance : ResultsModel = ResultsModel.construct_session();

    private static construct_session() : ResultsModel {
        let rankedList: Location[] = [];
        let str = window.sessionStorage.getItem('ResultsModel.rankedList');
        if(str) {
            rankedList = JSON.parse(str);
            if(rankedList) rankedList.forEach(location => {(location as any).__proto__ = Location.prototype});
        }

        let result = new ResultsModel();
        result.rankedList.set(rankedList);
        return result;
    }

    static getInstance() : ResultsModel {
        return this.resultsModelInstance;
    }

    private constructor() { 
        this.#rankedList.subscribe(rankedList => {
            if(rankedList) window.sessionStorage.setItem('ResultsModel.rankedList', JSON.stringify(rankedList));
            else window.sessionStorage.removeItem('ResultsModel.rankedList');
        });
    }

    #rankedList: Writable<Location[]> = writable();
    
    get rankedList() { return this.#rankedList }

    async getRankedList(filter: Filter) : Promise<Location[]> {        
        const url = new URL('api/locations/', `${window.location.protocol}//${window.location.host}`);
        for (const field in filter) {
            if(filter[field] !== null) url.searchParams.append(field, filter[field]);
        }
        const response = await fetch(url, RequestOptions.getRequestOptions());
        if(!response.ok) throw new RequestError(response.status, response.statusText);
        
        const res = await response.json();
        this.#rankedList.set(this.fixLocations(res));
        return get(this.#rankedList);
    }

    private fixLocations(list: any[]) : Location[] {
        return list.map(location => {return new Location(location.id, location.name, new Position(location.lat, location.long), 
                                                         location.address, location.maps_place_id, location.score)})
    }

    getById(id: number) : Location {
        return get(this.#rankedList).find(location => {return location.id == id});
    }
}
