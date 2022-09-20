import { writable, Writable } from "svelte/store";
import { AccountModel } from "../models/accountModel";

export class HomePresenter {
    #mapView: Writable<boolean> = writable(null);

    get mapView() { return this.#mapView }

    constructor() {
        const account = AccountModel.getInstance().getAccount();
        this.#mapView.set(!account.preference);
    }
}
