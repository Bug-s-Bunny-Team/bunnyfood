//import { Account } from "src/models";
import { AccountModel } from "../models/accountModel";

export class LoginPresenter {
    username: string;
    password: string;
    remember: boolean;

    constructor() {
        this.rememberFields = this.rememberFields.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
    }

    rememberFields() : void {
        if(AccountModel.getInstance().getAccount()) AccountModel.getInstance().cambiaRemember(this.remember);
    } 

    handleLogin() : void {
        const accModel = AccountModel.getInstance();
        if(this.checkUsername() && this.checkPassword())
        //Todo:
        //Controllo se username esiste ok altrimenti errore username, 
        //se la password non corrisponde allora errore psw
        accModel.login(this.username, this.password, this.remember);
    }

    checkUsername() : boolean {
        if(this.username) return true;
        //Todo:
        //controllo se username non esiste nel db
    }

    checkPassword() : boolean {
        if(this.password) return true;
    }
}
