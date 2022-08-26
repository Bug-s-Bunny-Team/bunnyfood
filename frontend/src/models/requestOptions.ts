import type { Account } from "../models";
import { AccountModel } from "./accountModel";

export class RequestOptions {
    static #get_request_options: RequestInit = {
        method: 'GET',
        mode: 'same-origin',
        credentials: 'include',
        headers: {
            'Authorization': "",
        }
    };

    static #post_request_options: RequestInit = {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'include',
        headers: {
            'Authorization': "",
            'Content-Type': 'application/json'
        },
        body: ""
    };

    static getRequestOptions(account: Account = null) : RequestInit {
        if(!account) account = AccountModel.getInstance().getAccount();
        if(!account) return null;
        const options = this.#get_request_options;
        options.headers['Authorization'] = 'Bearer ' + account.idtoken;
        return options;
    }

    static postRequestOptions(account: Account = null) {
        if(!account) account = AccountModel.getInstance().getAccount();
        if(!account) return null;
        const options = this.#post_request_options;
        options.headers['Authorization'] = 'Bearer ' + account.idtoken;
        return options;
    }
}