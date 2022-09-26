import { AccountModel } from "../../../src/models/accountModel";
import { expect, test, beforeAll, describe, jest } from '@jest/globals'
import { Account, RequestError } from '../../../src/models';

const mock_idtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2NjQwMjE0NDksImV4cCI6MTY5NTU1NzQ0OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsImVtYWlsIjoidGVzdEBnbWFpbC5jb20ifQ.QeUGbaE3XT-bcS2gI8bbFjFBrVv7xuOvHlbamr7k3Cw';
const mock_accesstoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2NjQwMjE0NDksImV4cCI6MTY5NTU1NzQ0OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsInVzZXJuYW1lIjoidGVzdCB1c2VybmFtZSJ9.g_ypyq8Fd_0U8zmrTUnLIP5RuK1Xx0ht6fqCi-cbogA'

describe('TUF17', () => {
    describe('1 - Session Storage update', () => {
        test('account defined', async () => {
            AccountModel.getInstance().account.set(new Account());
            expect((window.sessionStorage as any).getItem('AccountModel.account')).toBeTruthy();
        })

        test('account not defined', () => {
            AccountModel.getInstance().account.set(null as any);
            expect((window.sessionStorage as any).getItem('AccountModel.account')).toBeFalsy();     
        })
    })

    describe('2 - createAccount', () => {
        test('parameters present', async () => {
            const url = new URL(window.location.href);
            url.searchParams.append('id_token', mock_idtoken);
            url.searchParams.append('access_token', mock_accesstoken);
            window.location.href = url.toString().replace('?', '#');
            AccountModel.getInstance().logout();
            expect(AccountModel.getInstance().getAccount()).toBeFalsy();
            await AccountModel.getInstance().createAccount();
            expect(AccountModel.getInstance().getAccount()).toBeTruthy();
            await Account.schema.validate(AccountModel.getInstance().getAccount());
        })

        test('parameters not present', async () => {
            const url = new URL(window.location.href.replace('#', '?'));
            url.searchParams.delete('id_token');
            url.searchParams.delete('access_token');
            window.location.href = url.toString().replace('?', '#');
            AccountModel.getInstance().logout();
            expect(AccountModel.getInstance().getAccount()).toBeFalsy();
            await AccountModel.getInstance().createAccount();
            expect(AccountModel.getInstance().getAccount()).toBeFalsy();
        })
    })

    describe('3 - getAccount', () => {
        test('logged', () => {
            AccountModel.getInstance().account.set(new Account());
            expect(AccountModel.getInstance().getAccount()).toEqual(new Account());
        })

        test('not logged', () => {
            AccountModel.getInstance().account.set(null as any);
            expect(AccountModel.getInstance().getAccount()).toEqual(null as any);
        })
    })

    describe.each([true, false])('4 - cambiaPreferenza', preference => {
        beforeAll(() => {
            AccountModel.getInstance().account.set(new Account(mock_idtoken, mock_accesstoken, 'test accountname', 'test@gmail.com', true));
        })
        test('integration', async () => {
            try { await AccountModel.getInstance().cambiaPreferenza(preference) } 
            catch (e) { if(!(await RequestError.schema.isValid(e))) throw e; }
        })
        test('function', async () => {
            let promise = AccountModel.getInstance().cambiaPreferenza(preference);
            await expect(promise).resolves.not.toThrow();
        })
    })

    test('5 - logout', () => {
        AccountModel.getInstance().account.set(new Account(mock_idtoken, mock_accesstoken, 'test accountname', 'test@gmail.com', true));
        expect(AccountModel.getInstance().getAccount()).toBeTruthy();
        AccountModel.getInstance().logout();
        expect(AccountModel.getInstance().getAccount()).toBeFalsy();
    })
})