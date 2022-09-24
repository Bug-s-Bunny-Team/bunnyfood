import { init, fetch } from '../../integration/integration'
import { expect, test, beforeAll, describe, jest } from '@jest/globals'
import { ResultsModel } from '../../../src/models/resultsModel'
import { RequestError, Location, Filter } from '../../../src/models';
import { AccountModel } from '../../../src/models/accountModel';

jest.mock('../../../src/models/accountModel')

beforeAll(async () => {
    await init();
    window.fetch = fetch;
    await AccountModel.getInstance().createAccount();
})

const filter_test_cases = [
    new Filter(false, 2.0, 35.1, 10000.0, 0.0),
    new Filter(false, null as any, null as any, null as any, 0.0)
]

describe('TUF11', () => {
    describe('1 - Session Storage update', () => {
        test('rankedList defined', async () => {
            ResultsModel.getInstance().rankedList.set([]);
            expect((window.sessionStorage as any).getItem('ResultsModel.rankedList')).toBeTruthy();
        })

        test('rankedList not defined', () => {
            ResultsModel.getInstance().rankedList.set(null as any);
            expect((window.sessionStorage as any).getItem('ResultsModel.rankedList')).toBeFalsy();     
        })
    })

    describe.each(filter_test_cases)('2 - getRankedList', filter => {
        test('integration', async () => {
            try { await ResultsModel.getInstance().getRankedList(filter) } 
            catch (e) { if(!(await RequestError.schema.isValid(e))) throw e; }
        })
        test('function', async () => {
            let promise = ResultsModel.getInstance().getRankedList(filter);
            
            await expect(promise).resolves.not.toThrow();
            
            let locations = await promise;
            expect(locations.length).toBeGreaterThan(0);
            await Promise.all(locations.map(async profile => {
                await Location.schema.validate(profile); 
            }));
        })
    })

    describe('3 - getById', () => {
        test('to be found', async () => {
            const rankedList = await ResultsModel.getInstance().getRankedList(filter_test_cases[0]);
            rankedList.forEach(location => {
                expect(ResultsModel.getInstance().getById(location.id)).toBeTruthy();
            })
        })

        test('not to be found', async () => {
            const rankedList = await ResultsModel.getInstance().getRankedList(filter_test_cases[0]);
            for(let i=1; i<10; ++i) {
                expect(ResultsModel.getInstance().getById(rankedList[rankedList.length-1].id+i)).toBeFalsy();
            }
        })
    })
})