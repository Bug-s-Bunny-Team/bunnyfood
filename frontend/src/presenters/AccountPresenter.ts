import type { Account } from "../models";
import { writable, Writable } from "svelte/store";
import { AccountModel } from "../models/accountModel";

export class AccountPresenter {
    name: string;
    email: string;
    preference: number;
    isLogged: boolean;
    disableButtons: Writable<boolean> = writable(false);

    constructor() {
        this.changePreference = this.changePreference.bind(this);
        this.updateAccount = this.updateAccount.bind(this);
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
        window.location.href = "https://bunnyfood-dev.auth.eu-central-1.amazoncognito.com/logout?client_id=2k5d4g58072evbdqloqkuksd5u&response_type=token&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F";
        AccountModel.getInstance().logout();
    }

    changePreference() : void {
        if(this.isLogged) {
            this.disableButtons.set(true);
            AccountModel.getInstance().cambiaPreferenza(Boolean(!this.preference)).then(() => {this.disableButtons.set(false)});
        }
    }

}
