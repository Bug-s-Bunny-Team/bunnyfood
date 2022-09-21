import type { Account, RequestError } from "../models";
import { get, writable, Writable } from "svelte/store";
import { AccountModel } from "../models/accountModel";
import { error_duration, removeChildren } from "../utils";
import ErrorSvelte from "../components/Error.svelte";

export class AccountPresenter {
    #name: Writable<string> = writable(null);
    #email: Writable<string> = writable(null);
    #preference: Writable<number> = writable(null);
    #isLogged: Writable<boolean> = writable(false);
    #disableButtons: Writable<boolean> = writable(false);
    #errorTimeout: NodeJS.Timeout = null;

    get name() { return this.#name }
    get email() { return this.#email }
    get preference() { return this.#preference }
    get isLogged() { return this.#isLogged }
    get disableButtons() { return this.#disableButtons }

    constructor() {
        this.changePreference = this.changePreference.bind(this);
        this.updateAccount = this.updateAccount.bind(this);
        this.destroy = this.destroy.bind(this);
        this.logout = this.logout.bind(this);
        AccountModel.getInstance().account.subscribe(this.updateAccount);
    }

    private updateAccount(account: Account) {
        this.#isLogged.set(account ? true : false);
        if(account) {
            this.#name.set(account.accountname);
            this.#email.set(account.email);
            this.#preference.set(account.preference ? 1 : 0);
        }
    }

    logout() {
        this.#disableButtons.set(true);
        const redirect_url = encodeURIComponent(`${window.location.protocol}//${window.location.host}/`);
        window.location.href = `https://bunnyfood-dev.auth.eu-central-1.amazoncognito.com/logout?client_id=2k5d4g58072evbdqloqkuksd5u&response_type=token&redirect_uri=${redirect_url}`;
        AccountModel.getInstance().logout();
    }

    changePreference() : void {
        if(get(this.isLogged)) {
            this.#disableButtons.set(true);
            AccountModel.getInstance().cambiaPreferenza(!(get(this.#preference) == 1 ? true : false))
                .catch((e: RequestError) => { 
                    removeChildren(document.getElementById('error')); 
                    const message = 'An error occurred, please try again';
                    new ErrorSvelte({props: {message: message}, target: document.getElementById('error')});
                    this.#errorTimeout = setTimeout(() => {removeChildren(document.getElementById('error'))}, error_duration);
                })
                .finally(() => {this.#disableButtons.set(false)});
        }
    }

    destroy() {
        if(this.#errorTimeout) {
          removeChildren(document.getElementById('error'));
          clearTimeout(this.#errorTimeout)
        } 
    }
}
