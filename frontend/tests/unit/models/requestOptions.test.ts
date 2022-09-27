import { expect, test, beforeAll, describe, jest } from '@jest/globals'
import { Account } from '../../../src/models'
import { AccountModel } from '../../../src/models/accountModel'
import { RequestOptions } from '../../../src/models/requestOptions'

jest.mock('../../../src/models/accountModel')

describe('TUF15', () => {
    describe('not logged', () => {
        beforeAll(() => {
            AccountModel.getInstance().logout();
        })

        test('1 - getRequestOptions', () => {
            const options = RequestOptions.getRequestOptions();
            expect(options).toBeFalsy();
        })
    
        test('2 - postRequestOptions', () => {
            const options = RequestOptions.postRequestOptions();
            expect(options).toBeFalsy();
        })
    })

    describe('logged', () => {
        beforeAll(async () => {
            await AccountModel.getInstance().createAccount();
        })

        test('1 - getRequestOptions', () => {
            const options = RequestOptions.getRequestOptions() as any;
            expect(options).toBeTruthy();
            expect(options.headers['Authorization']).toMatch(/Bearer [a-z,A-Z,0-9]{27}/);
        })
    
        test('2 - postRequestOptions', () => {
            const options = RequestOptions.postRequestOptions() as any;
            expect(options).toBeTruthy();
            expect(options.headers['Authorization']).toMatch(/Bearer [a-z,A-Z,0-9]{27}/);
        })
    })

    describe('from new account', () => {
        const acc = new Account("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2NjQwMjE0NDksImV4cCI6MTY5NTU1NzQ0OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsImVtYWlsIjoidGVzdEBnbWFpbC5jb20ifQ.QeUGbaE3XT-bcS2gI8bbFjFBrVv7xuOvHlbamr7k3Cw", 
                                "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2NjQwMjE0NDksImV4cCI6MTY5NTU1NzQ0OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsInVzZXJuYW1lIjoidGVzdCB1c2VybmFtZSJ9.g_ypyq8Fd_0U8zmrTUnLIP5RuK1Xx0ht6fqCi-cbogA", 
                                "test user", 
                                "test email", 
                                true);

        test('1 - getRequestOptions', () => {
            const options = RequestOptions.getRequestOptions(acc) as any;
            expect(options).toBeTruthy();
            expect(options.headers['Authorization']).toMatch(/^Bearer [A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$/);
        })
    
        test('2 - postRequestOptions', () => {
            const options = RequestOptions.postRequestOptions(acc) as any;
            expect(options).toBeTruthy();
            expect(options.headers['Authorization']).toMatch(/^Bearer [A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$/);
        })
    })

})