import { jest, test, expect, beforeEach, describe } from '@jest/globals';
import { get } from 'svelte/store';
import { ListPresenter } from '../../../src/presenters/ListPresenter'

jest.mock('../../../src/models/resultsModel');

beforeEach(() => {
    jest.clearAllMocks();
})

describe('TUF3', () => {
    test('1 - constructor', () => {
        const tmp = ListPresenter.prototype.refresh;
        ListPresenter.prototype.refresh = jest.fn();
        
        new ListPresenter();
        expect(ListPresenter.prototype.refresh).toHaveBeenCalledTimes(1);
    
        ListPresenter.prototype.refresh = tmp;
    })
    
    test('2 - refresh', async () => {
        let presenter = new ListPresenter();
        await get(presenter.rankedList);
    
        expect(get(presenter.disableButtons)).toStrictEqual(false);
        presenter.refresh();
        expect(get(presenter.disableButtons)).toStrictEqual(true);
    
        const list_prom = get(presenter.rankedList);
        expect(list_prom).toBeTruthy();
        const list = await list_prom;
        expect(get(presenter.disableButtons)).toStrictEqual(false);
    
        expect(list.length).toBeGreaterThan(0);
        list.forEach(location => {
            expect(location).toBeTruthy();
            expect(location.id).toBeGreaterThanOrEqual(0);
            expect(location.name).toBeTruthy();
            expect(location.position).toBeTruthy();
            expect(location.position.lat).toBeTruthy();
            expect(location.position.long).toBeTruthy();
            expect(location.score).not.toStrictEqual(undefined);
            expect(location.address).toBeTruthy();
            expect(location.maps_place_id).toBeTruthy();
        })
    })
})