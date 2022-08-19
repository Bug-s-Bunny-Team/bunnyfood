import type { Location, Position } from '../models'

export class Filter {
    globale: boolean;
    posizione: Position;
    n_risultati: number;
    raggio: number;
    min_rating: number;
}

export class ResultsModel {
    private static resultsModelInstance : ResultsModel = ResultsModel.construct_session();

    private static construct_session() : ResultsModel {
        let result = new ResultsModel();
        return result;
    }

    static getInstance() : ResultsModel {
        return this.resultsModelInstance;
    }

    private constructor() { 
    }

    private static static_delay_ms = 200;
    
    async getRankedList(filter: Filter) : Promise<Location[]> {
        await new Promise(r => setTimeout(r, ResultsModel.static_delay_ms))
        const response = await fetch('dev-api/results');
        return await response.json();
    }
}
