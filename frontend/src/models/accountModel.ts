import { Writable, writable, get } from 'svelte/store';
import { Account } from '../models'

export class AccountModel {
    private static accountModelInstance : AccountModel = AccountModel.construct_session();

    private static construct_session() : AccountModel {
        let account: Account = null;
        let str = window.sessionStorage.getItem('AccountModel.account');
        if(str) {
            account = JSON.parse(str);
            if(account) account.__proto__ = Account.prototype; // errore del compilatore don't worry
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
        })
    }

    account: Writable<Account> = writable();
    
    login(email: string, password: string, remember: boolean): void {
        this.account.set(new Account("nome default", email, password, true));
    }
    
    registrati(email: string, password: string): void {
        this.account.set(new Account("nome default", email, password, true));
    }
    
    logout() : void {
        this.account.set(null);
    }
    
    cambiaPsw(psw_new: string) : void {
        this.account.update(() => { let account = this.getAccount(); account.password = psw_new; return account; });
    }

    cambiaPreferenza(newPref: boolean) {
        this.account.update(() => { let account = this.getAccount(); account.preference = newPref; return account; });
    }

    cambiaRemember(newRem: boolean) {
        this.account.update(() => { let account = this.getAccount(); account.remember = newRem; return account; });
    }

    getAccount() {
        return get(this.account);
    }

}
