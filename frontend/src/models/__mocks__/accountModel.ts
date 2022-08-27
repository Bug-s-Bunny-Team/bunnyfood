import { Writable, writable, get } from 'svelte/store';
import { Account } from '../../models'

export class AccountModel {
    private static accountModelInstance : AccountModel = AccountModel.construct_session();

    private static construct_session() : AccountModel {
        return new AccountModel();
    }

    static getInstance() : AccountModel {
        return this.accountModelInstance;
    }

    private constructor() {}

    account: Writable<Account> = writable();
    
    async createAccount(): Promise<void> {
        this.account.set(new Account("", "", "mock accountname", "mock email", false));
    }

    async cambiaPreferenza(newPref: boolean) : Promise<void> {        
        this.account.update(account => { account.preference = newPref; return account; });
    }

    logout() : void {
        this.account.set(null);
    }

    getAccount() {
        return get(this.account);
    }
}
