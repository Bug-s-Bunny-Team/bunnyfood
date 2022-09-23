import { jest, test, expect, beforeEach, describe } from '@jest/globals';
import { get } from 'svelte/store';
import { Location } from '../../../src/models';
import { ResultsModel } from '../../../src/models/resultsModel';
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
        expect(ResultsModel.getInstance().getRankedList).toHaveBeenCalledTimes(1);
    
        expect(get(presenter.disableButtons)).toStrictEqual(false);
        presenter.refresh();
        expect(get(presenter.disableButtons)).toStrictEqual(true);
    
        const list_prom = get(presenter.rankedList);
        expect(list_prom).toBeTruthy();
        await list_prom;
        expect(get(presenter.disableButtons)).toStrictEqual(false);
        expect(ResultsModel.getInstance().getRankedList).toHaveBeenCalledTimes(2);
    })
})