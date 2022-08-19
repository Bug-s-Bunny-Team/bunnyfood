import { AccountModel } from "../models/accountModel";

export class ChangePswPresenter {
    confirmPsw: string;
    NewPsw: string;

    constructor() {
        this.handleChangePsw = this.handleChangePsw.bind(this);
    }

    handleChangePsw() : void {
        const accModel = AccountModel.getInstance();
        if(this.handleNewPsw() && this.handleConfirmPsw())
        //Todo:
        //Controllo se username esiste ok altrimenti errore username, 
        //se la password non corrisponde allora errore psw
            accModel.cambiaPsw(this.NewPsw);
    }

    handleNewPsw() : boolean {
        if(this.NewPsw) return true;
    }

    handleConfirmPsw() : boolean {
        if(this.NewPsw == this.confirmPsw) return true;
    }
}
