import { Writable, writable } from "svelte/store";
import { AccountModel } from "../models/accountModel";
import { routes } from "../routes";

export class NavPresenter {
    #routes: Writable<any[]> = writable();

    get routes() { return this.#routes }

    constructor() {
        AccountModel.getInstance().account.subscribe(account => {
            if(account) { this.#routes.set(routes); }
            else { this.#routes.set([]); }
        })
    }
}
