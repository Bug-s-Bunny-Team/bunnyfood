import { jest, test, expect, describe } from '@jest/globals';
import { get } from 'svelte/store';
import { AccountModel } from '../../../src/models/accountModel';
import { AppPresenter } from '../../../src/presenters/AppPresenter';

jest.mock('../../../src/models/accountModel');

describe('TUF6', () => {
    describe('1 - constructor', () => {
        test('logged', () => {
            let presenter = new AppPresenter();
            const routes = get(presenter.routes);
            expect(routes).toBeTruthy();
            expect(routes).toHaveLength(6);
        })
    
        test('not logged', () => {
            AccountModel.getInstance().logout();
            let presenter = new AppPresenter();
            const routes = get(presenter.routes);
            expect(routes).toBeTruthy();
            expect(routes).toHaveLength(6);
            AccountModel.getInstance().createAccount();
        })
    })
})