import { Writable, writable, get } from 'svelte/store';
import { Account } from '../../models'
import Preference from '../../../mock/preferences.json'

export class AccountModel {
    private static accountModelInstance : AccountModel = AccountModel.construct_session();

    private static construct_session() : AccountModel {
        return new AccountModel();
    }

    static getInstance() : AccountModel {
        return this.accountModelInstance;
    }

    private constructor() {}

    #account: Writable<Account> = writable();

    get account() { return this.#account }
    
    async createAccount(): Promise<void> {
        this.#account.set(new Account("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2NjQwMjE0NDksImV4cCI6MTY5NTU1NzQ0OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsImVtYWlsIjoidGVzdEBnbWFpbC5jb20ifQ.QeUGbaE3XT-bcS2gI8bbFjFBrVv7xuOvHlbamr7k3Cw", 
                                      "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2NjQwMjE0NDksImV4cCI6MTY5NTU1NzQ0OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsInVzZXJuYW1lIjoidGVzdCB1c2VybmFtZSJ9.g_ypyq8Fd_0U8zmrTUnLIP5RuK1Xx0ht6fqCi-cbogA", 
                                      "mock accountname", 
                                      "mock email", 
                                      Preference.default_guide_view == 'map' ? true : false));
    }

    cambiaPreferenza = jest.fn(async function(newPref: boolean) : Promise<void> {        
        this.#account.update((account: Account) => { account.preference = newPref; return account; });
    });

    logout = jest.fn(function () : void {
        this.#account.set(null);
    });

    getAccount() {
        return get(this.#account);
    }
}
