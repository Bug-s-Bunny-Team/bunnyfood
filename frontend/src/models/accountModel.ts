import { Writable, writable, get } from 'svelte/store';
import { Account } from '../models'

export class AccountModel {
    private static accountModelInstance : AccountModel = AccountModel.construct_session();

    private static construct_session() : AccountModel {
        let account: Account = null;
        let str = window.sessionStorage.getItem('AccountModel.account');
        if(str) {
            account = JSON.parse(str);
            if(account) (account as any).__proto__ = Account.prototype;
        }

        let result = new AccountModel();
        result.account.set(account);
        return result;
    }

    static getInstance() : AccountModel {
        return this.accountModelInstance;
    }

    private constructor() { 
        this.account.subscribe(account => {
            if(account) window.sessionStorage.setItem('AccountModel.account', JSON.stringify(account));
            else window.sessionStorage.removeItem('AccountModel.account');
        });
    }

    private static static_delay_ms = 200;

    static get_request_options: RequestInit = {
        method: 'GET',
        mode: 'same-origin',
        credentials: 'same-origin'
    };

    static post_request_options: RequestInit = {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
        },
        body: ""
    };

    account: Writable<Account> = writable();
    
    async createAccount(): Promise<void> {
        // TODO get jwt token, then request map/list preference
        await new Promise(r => setTimeout(r, AccountModel.static_delay_ms))
        
        const response = await fetch('dev-api/preferences', AccountModel.get_request_options);
        
        const res = await response.json();
        if(!response.ok) return;
        this.account.set(new Account(res.accountname, res.email, res.preferenza == "list" ? true : false));
    }

    async cambiaPreferenza(newPref: boolean) : Promise<void> {
        await new Promise(r => setTimeout(r, AccountModel.static_delay_ms))
        
        const options = AccountModel.post_request_options;
        options.method = 'PUT';
        options.body = JSON.stringify({default_guide_view: newPref == true ? 'list' : 'map'});
        const response = await fetch('dev-api/preferences', options);
        
        const res = await response.json();
        if(!response.ok) throw new Error(`Error ${res.code}: ${res.msg}`);

        this.account.update(() => { let account = this.getAccount(); account.preference = newPref; return account; });
    }

    getAccount() {
        return get(this.account);
    }

}
