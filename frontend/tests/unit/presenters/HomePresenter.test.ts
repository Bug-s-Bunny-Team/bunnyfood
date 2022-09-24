import { jest, test, expect, describe } from '@jest/globals';
import { get } from 'svelte/store';
import { AccountModel } from '../../../src/models/accountModel';
import { HomePresenter } from '../../../src/presenters/HomePresenter';

jest.mock('../../../src/models/accountModel');

describe('TUF7', () => {
    test('1 - constructor', async () => {
        await AccountModel.getInstance().createAccount();
        let presenter = new HomePresenter();
        expect(get(presenter.mapView)).toEqual(!get(AccountModel.getInstance().account).preference);
    })
})