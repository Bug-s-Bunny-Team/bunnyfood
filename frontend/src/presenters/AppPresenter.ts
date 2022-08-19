import { Writable, writable } from "svelte/store";
import { AccountModel } from "../models/accountModel";
import { routes } from "../routes";

export class AppPresenter {
    routes: Writable<any[]> = writable();

    constructor() {
        AccountModel.getInstance().account.subscribe(account => {
            this.routes.set(routes);
        })
    }
}
