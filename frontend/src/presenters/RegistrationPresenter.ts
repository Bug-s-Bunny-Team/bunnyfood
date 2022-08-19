import { AccountModel } from "../models/accountModel";

export class RegistrationPresenter {
    firstname: string;
    lastname: string;
    username: string;
    email: string;
    password: string;
    confirmPsw: string;

    constructor() {
        this.handleRegister = this.handleRegister.bind(this);
    }

    handleRegister() : void {
        const accModel = AccountModel.getInstance();
        if(this.handleNames() && this.handleEmail() && this.handlePassword()
                                 && this.handleConfirmPassword())
        //Todo:
        //Controllo 
            accModel.registrati(this.email, this.password);
    }

    handleNames(): boolean{
        if(this.firstname && this.lastname) return true;
    }

    handleUsername() : boolean {
        if(this.username) return true;
    }

    handleEmail() : boolean {
        if(this.email) return true;
        //Todo:
        //controllo email nel sistema se esiste già e controllo email valida
    }

    handlePassword() : boolean {
        if(this.password) return true;
    }

    handleConfirmPassword() : boolean {
        if(this.password == this.confirmPsw) return true;
    }
}
