import { jest, test, expect, describe } from '@jest/globals';
import { get } from 'svelte/store';
import { AccountModel } from '../../../src/models/accountModel';
import { NavPresenter } from '../../../src/presenters/NavPresenter';

jest.mock('../../../src/models/accountModel');

describe('TUF5', () => {
    describe('1 - constructor', () => {
        test('logged', async () => {
            await AccountModel.getInstance().createAccount();
            let presenter = new NavPresenter();
            const routes = get(presenter.routes);
            expect(routes).toBeTruthy();
            expect(routes).toHaveLength(6);
        })
    
        test('not logged', () => {
            AccountModel.getInstance().logout();
            let presenter = new NavPresenter();
            const routes = get(presenter.routes);
            expect(routes).toBeTruthy();
            expect(routes).toHaveLength(0);
        })
    })
})