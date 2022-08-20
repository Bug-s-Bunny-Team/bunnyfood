import type { Info } from "../models";
import { LocationModel } from "../models/locationModel";
import { writable, Writable } from "svelte/store";

export class LocationPresenter {
    #id: number;
    info: Writable<Promise<Info>> = writable();

    constructor(id: number) {
        this.#id = id;
        this.getInfo = this.getInfo.bind(this);
        this.getInfo();
    }

    getInfo() : void {
        this.info.set(this.adjustInfo(LocationModel.getInstance().getInfo(this.#id)))
    }

    async adjustInfo(info: Promise<Info>) : Promise<Info> {
        let _info: Info = await info;
        _info.name = this.capitalizeFirstLetter(_info.name);
        _info.address = this.capitalizeFirstLetter(_info.address);
        return _info;
    }

    private capitalizeFirstLetter(string: string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
}