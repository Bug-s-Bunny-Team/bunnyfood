import { jest, test, describe, expect, beforeEach } from '@jest/globals';
import { get } from 'svelte/store';
import { ListPresenter } from '../../../src/presenters/ListPresenter'

jest.mock('../../../src/models/resultsModel');

describe('ListPresenter', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    })

    test('constructor', () => {
        const tmp = ListPresenter.prototype.refresh;
        ListPresenter.prototype.refresh = jest.fn();
        
        new ListPresenter();
        expect(ListPresenter.prototype.refresh).toHaveBeenCalledTimes(1);

        ListPresenter.prototype.refresh = tmp;
    })

    test('refresh', async () => {
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
            expect(location.score).toBeGreaterThanOrEqual(0.0);
        })
    })
})