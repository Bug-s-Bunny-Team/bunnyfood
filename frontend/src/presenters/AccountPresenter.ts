import type { Account, RequestError } from "../models";
import { writable, Writable } from "svelte/store";
import { AccountModel } from "../models/accountModel";
import { error_duration, removeChildren } from "../utils";
import ErrorSvelte from "../components/Error.svelte";

export class AccountPresenter {
    name: string;
    email: string;
    preference: number;
    isLogged: boolean;
    disableButtons: Writable<boolean> = writable(false);
    errorTimeout: NodeJS.Timeout = null;

    constructor() {
        this.changePreference = this.changePreference.bind(this);
        this.updateAccount = this.updateAccount.bind(this);
        this.destroy = this.destroy.bind(this);
        AccountModel.getInstance().account.subscribe(this.updateAccount);
    }

    private updateAccount(account: Account) {
        this.isLogged = account ? true : false;
        if(account) {
            this.name = account.accountname;
            this.email = account.email;
            this.preference = Number(account.preference);
        }
    }

    logout() {
        const redirect_url = encodeURIComponent(`${window.location.protocol}//${window.location.host}/`);
        window.location.href = `https://bunnyfood-dev.auth.eu-central-1.amazoncognito.com/logout?client_id=2k5d4g58072evbdqloqkuksd5u&response_type=token&redirect_uri=${redirect_url}`;
        AccountModel.getInstance().logout();
    }

    changePreference() : void {
        if(this.isLogged) {
            this.disableButtons.set(true);
            AccountModel.getInstance().cambiaPreferenza(Boolean(!this.preference))
                .catch((e: RequestError) => { 
                    removeChildren(document.getElementById('error')); 
                    const message = 'An error occurred, please try again';
                    new ErrorSvelte({props: {message: message}, target: document.getElementById('error')});
                    this.errorTimeout = setTimeout(() => {removeChildren(document.getElementById('error'))}, error_duration);
                })
                .finally(() => {this.disableButtons.set(false)});
        }
    }

    destroy() {
        if(this.errorTimeout) clearTimeout(this.errorTimeout);
    }
}
