import { Writable, writable, get } from 'svelte/store';
import { Account, RequestError } from '../models'
import 'jwt-decode'
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

    private static static_delay_ms = 200;

    #get_request_options: RequestInit = {
        method: 'GET',
        mode: 'same-origin',
        credentials: 'include',
        headers: {
            'Authorization': "",
        }
    };

    #post_request_options: RequestInit = {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'include',
        headers: {
            'Authorization': "",
            'Content-Type': 'application/json'
        },
        body: ""
    };

    account: Writable<Account> = writable();
    
    async createAccount(): Promise<void> {
        await new Promise(r => setTimeout(r, AccountModel.static_delay_ms))

        const params = this.getSearchParams();
        const idtoken = params.get('id_token');
        const accesstoken = params.get('access_token');
        
        if(!idtoken || !accesstoken) return;
        const id_decoded: any = jwtDecode(idtoken);
        const access_decoded: any = jwtDecode(accesstoken);
        const account = new Account(idtoken, accesstoken, access_decoded.username, id_decoded.email, null);
        
        const response = await fetch('dev-api/preferences', this.getRequestOptions(account));
        
        const res = await response.json();
        if(!response.ok) return;
        account.preference = res.default_guide_view == "list" ? true : false;
        this.account.set(account);
    }

    async cambiaPreferenza(newPref: boolean) : Promise<void> {
        await new Promise(r => setTimeout(r, AccountModel.static_delay_ms))
        
        const options = this.postRequestOptions();
        options.method = 'PUT';
        options.body = JSON.stringify({default_guide_view: newPref == true ? 'list' : 'map'});
        const response = await fetch('dev-api/preferences', options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);

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

    postRequestOptions(account: Account = null) : RequestInit {
        if(!account) account = this.getAccount();
        const options = this.#post_request_options;
        options.headers['Authorization'] = 'Bearer ' + account.idtoken;
        return options;
    }

    getRequestOptions(account: Account = null) : RequestInit {
        if(!account) account = this.getAccount();
        const options = this.#get_request_options;
        options.headers['Authorization'] = 'Bearer ' + account.idtoken;
        return options;
    }
}