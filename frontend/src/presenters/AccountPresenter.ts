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

    changePreference() : void {
        if(this.isLogged) {
            this.disableButtons.set(true);
            AccountModel.getInstance().cambiaPreferenza(Boolean(!this.preference)).then(() => {this.disableButtons.set(false)});
        }
    }

}
