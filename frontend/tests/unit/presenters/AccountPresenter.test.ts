import { jest, test, expect, beforeEach, describe } from '@jest/globals';
import { get } from 'svelte/store';
import { RequestError } from '../../../src/models';
import { AccountModel } from '../../../src/models/accountModel';
import { AccountPresenter } from '../../../src/presenters/AccountPresenter'
import { removeChildren } from '../../../src/utils';

jest.mock('../../../src/models/accountModel');

(AccountModel.getInstance().cambiaPreferenza as any) .mockResolvedValueOnce(undefined)
                                                     .mockRejectedValueOnce(new RequestError(400, "a"))
                                                     .mockRejectedValueOnce(new RequestError(400, "a"));

jest.useFakeTimers();

beforeEach(async () => {
    removeChildren((document.getElementById('error') as HTMLElement));
    jest.clearAllTimers();
    jest.clearAllMocks();
    await AccountModel.getInstance().createAccount();
})

describe('TUF9', () => {

    describe('1 - constructor', () => {
        test('logged', () => {
            const account = get(AccountModel.getInstance().account);
            const presenter = new AccountPresenter();
            expect(get(presenter.isLogged)).toStrictEqual(true);
            expect(get(presenter.name)).toStrictEqual(account.accountname);
            expect(get(presenter.email)).toStrictEqual(account.email);
            expect(get(presenter.preference) === 1).toStrictEqual(account.preference);
        })

        test('not logged', async () => {
            AccountModel.getInstance().logout();
            const presenter = new AccountPresenter();
            expect(get(presenter.isLogged)).toStrictEqual(false);
            expect(get(presenter.name)).toStrictEqual(null);
            expect(get(presenter.email)).toStrictEqual(null);
            expect(get(presenter.preference)).toStrictEqual(null);
        })
    })

    describe('2 - responsiveness', () => {
        test('logged -> not logged', async () => {
            const presenter = new AccountPresenter();

            AccountModel.getInstance().logout();
            expect(get(presenter.isLogged)).toStrictEqual(false);
            expect(get(presenter.name)).toStrictEqual(null);
            expect(get(presenter.email)).toStrictEqual(null);
            expect(get(presenter.preference)).toStrictEqual(null);
        })

        test('not logged -> logged', async () => {
            AccountModel.getInstance().logout();
            const presenter = new AccountPresenter();

            await AccountModel.getInstance().createAccount();
            const account = get(AccountModel.getInstance().account);
            expect(get(presenter.isLogged)).toStrictEqual(true);
            expect(get(presenter.name)).toStrictEqual(account.accountname);
            expect(get(presenter.email)).toStrictEqual(account.email);
            expect(get(presenter.preference) === 1).toStrictEqual(account.preference);
        })
    })
    
    // cannot test because the test environment jsdom does not support window.location navigation, so the function fails with "Error: Not implemented: navigation (except hash changes)"
    /*test('3 - logout', async () => {
        const presenter = new AccountPresenter();
        const url = window.location.href;

        expect(get(presenter.disableButtons)).toStrictEqual(false);
        presenter.logout();
        expect(get(presenter.disableButtons)).toStrictEqual(true);
        expect(window.location.href).not.toEqual(url);
        expect(AccountModel.getInstance().logout).toHaveBeenCalledTimes(1);    
    })*/

    describe('4 - changePreference', () => {
        test('noexcept', async () => {
            const presenter = new AccountPresenter();

            let promise = presenter.changePreference();
            expect(AccountModel.getInstance().cambiaPreferenza).toHaveBeenCalledTimes(1);
            expect(AccountModel.getInstance().cambiaPreferenza).toHaveBeenLastCalledWith(!(get(presenter.preference) == 1 ? true : false));
            expect(get(presenter.disableButtons)).toStrictEqual(true);
            
            await expect(promise).resolves.toStrictEqual(undefined);
            expect((document.getElementById('error') as HTMLElement).childElementCount).toStrictEqual(0); // no errors
            expect(get(presenter.disableButtons)).toStrictEqual(false);
            expect(jest.getTimerCount()).toStrictEqual(0);
        })

        test('exception', async () => {
            const presenter = new AccountPresenter();
        
            let promise = presenter.changePreference();
            expect(AccountModel.getInstance().cambiaPreferenza).toHaveBeenCalledTimes(1);
            expect(AccountModel.getInstance().cambiaPreferenza).toHaveBeenLastCalledWith(!(get(presenter.preference) == 1 ? true : false));
            expect(get(presenter.disableButtons)).toStrictEqual(true);
            
            await expect(promise).resolves.toStrictEqual(undefined);
            expect((document.getElementById('error') as HTMLElement).childElementCount).toStrictEqual(1); // one error
            expect(get(presenter.disableButtons)).toStrictEqual(false);
            expect(jest.getTimerCount()).toStrictEqual(1);

            jest.runAllTimers();

            expect(jest.getTimerCount()).toStrictEqual(0);
            expect((document.getElementById('error')as HTMLElement).childElementCount).toStrictEqual(0); // error removed
        })
    })

    describe('5 - destroy', () => {
        test('running timer', async () => {
            const presenter = new AccountPresenter();

            await presenter.changePreference();
            expect(jest.getTimerCount()).toStrictEqual(1);
            expect((document.getElementById('error') as HTMLElement).childElementCount).toStrictEqual(1); // one error
            
            presenter.destroy();
            
            expect(jest.getTimerCount()).toStrictEqual(0);
            expect((document.getElementById('error') as HTMLElement).childElementCount).toStrictEqual(0); // error removed
        })

        test('no running timer', () => {
            const presenter = new AccountPresenter();
            
            presenter.destroy();

            expect(jest.getTimerCount()).toStrictEqual(0);
            expect((document.getElementById('error') as HTMLElement).childElementCount).toStrictEqual(0); // error removed
        })
    })
})