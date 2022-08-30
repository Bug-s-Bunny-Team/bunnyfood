import { Writable, writable, get } from 'svelte/store';
import { Account, RequestError } from '../models'
import { RequestOptions } from './requestOptions';
import jwtDecode from 'jwt-decode';

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

    account: Writable<Account> = writable();
    
    async createAccount(): Promise<void> {
        const params = this.getSearchParams();
        const idtoken = params.get('id_token');
        const accesstoken = params.get('access_token');
        
        if(!idtoken || !accesstoken) return;
        const id_decoded: any = jwtDecode(idtoken);
        const access_decoded: any = jwtDecode(accesstoken);
        const account = new Account(idtoken, accesstoken, access_decoded.username, id_decoded.email, null);
        
        const response = await fetch('api/preferences/', RequestOptions.getRequestOptions(account));
        if(!response.ok) throw new RequestError(response.status, response.statusText);

        const res = await response.json();
        account.preference = res.default_guide_view == "list" ? true : false;
        this.account.set(account);
    }

    async cambiaPreferenza(newPref: boolean) : Promise<void> {        
        const options = RequestOptions.postRequestOptions();
        options.method = 'PUT';
        options.body = JSON.stringify({default_guide_view: newPref == true ? 'list' : 'map'});
        const response = await fetch('api/preferences/', options);
        if(!response.ok) throw new RequestError(response.status, response.statusText);
        this.account.update(account => { account.preference = newPref; return account; });
    }

    logout() : void {
        this.account.set(null);
    }

    getAccount() {
        return get(this.account);
    }

    private getSearchParams() : URLSearchParams {
        const url = new URL(window.location.href.replace('#', '?'));
        return url.searchParams;
    }
}
