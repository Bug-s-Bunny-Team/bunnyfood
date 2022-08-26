import { get, Writable, writable } from 'svelte/store';
import { Filter, Location, Position, RequestError } from '../models'

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
        this.rankedList.subscribe(rankedList => {
            if(rankedList) window.sessionStorage.setItem('ResultsModel.rankedList', JSON.stringify(rankedList));
            else window.sessionStorage.removeItem('ResultsModel.rankedList');
        });
    }

    static request_options: RequestInit = {
        method: 'GET',
        mode: 'same-origin',
        credentials: 'same-origin'
    };

    rankedList: Writable<Location[]> = writable();

    private static static_delay_ms = 200;
    
    async getRankedList(filter: Filter) : Promise<Location[]> {
        await new Promise(r => setTimeout(r, ResultsModel.static_delay_ms))
        
        const url = new URL('dev-api/locations', `${window.location.protocol}//${window.location.host}`);
        for (const field in filter) {
            url.searchParams.append(field, filter[field]);
        }
        const response = await fetch(url, ResultsModel.request_options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        this.rankedList.set(this.fixLocations(res));
        return get(this.rankedList);
    }

    fixLocations(list: any[]) : Location[] {
        return list.map(location => {return new Location(location.id, location.name, new Position(location.lat, location.long), location.score)})
    }

    getById(id: number) : Location {
        return get(this.rankedList).find(location => {return location.id == id});
    }
}
