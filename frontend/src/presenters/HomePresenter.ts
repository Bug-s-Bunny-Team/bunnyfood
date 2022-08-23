import { AccountModel } from "../models/accountModel";

export class HomePresenter {
    mapView: boolean = true;

    constructor() {
        const account = AccountModel.getInstance().getAccount();
        if(account) {
            this.mapView = !account.preference;
        }
    }
}
