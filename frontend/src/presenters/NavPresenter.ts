import { Writable, writable } from "svelte/store";
import { AccountModel } from "../models/accountModel";
import { PublicRoutes, ProtectedRoutes } from "../routes";

export class NavPresenter {
    routes: Writable<any[]> = writable();

    constructor() {
        AccountModel.getInstance().account.subscribe(account => {
            if(account) { this.routes.set(ProtectedRoutes); }
            else { this.routes.set(PublicRoutes); }
        })
    }
}
