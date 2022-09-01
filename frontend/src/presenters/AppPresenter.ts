import { Writable, writable } from "svelte/store";
import { routes } from "../routes";

export class AppPresenter {
    routes: Writable<any[]> = writable();

    constructor() {
        this.routes.set(routes);
    }
}
