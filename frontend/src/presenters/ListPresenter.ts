import { writable, Writable } from "svelte/store";
import { Filter, Location } from "../models";
import { ResultsModel } from "../models/resultsModel";

export class ListPresenter {
    rankedList: Writable<Promise<Location[]>> = writable(null);
    disableButtons: Writable<boolean> = writable(false);

    constructor() {
        this.refresh = this.refresh.bind(this);
        this.refresh();
    }

    refresh() : void {
        this.disableButtons.set(true);
        let promise = ResultsModel.getInstance().getRankedList(new Filter(false, null, null, null, 0.0));
        promise.finally(() => {this.disableButtons.set(false)});
        this.rankedList.set(promise);
    }
}
