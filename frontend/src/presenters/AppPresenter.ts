import { Writable, writable } from "svelte/store";
import { routes } from "../routes";

export class AppPresenter {
    #routes: Writable<any[]> = writable();

    get routes() { return this.#routes }

    constructor() {
        this.routes.set(routes);
    }
}
