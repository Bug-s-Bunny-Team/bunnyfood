import { Info, RequestError } from "../models";
import { LocationModel } from "../models/locationModel";
import { get, Unsubscriber, Writable, writable } from "svelte/store";
import { google_ready } from "../store";
import { capitalizeFirstLetter } from "../utils";

export class LocationPresenter {
    #id: number;
    #info: Writable<Promise<Info>> = writable();

    get info() { return this.#info }

    constructor(id: number) {
        this.#id = id;
        this.getInfo = this.getInfo.bind(this);
        this.getInfo();
    }

    getInfo() : void {
        this.#info.set(new Promise((resolve, reject) => {
            let unsubscribe: Unsubscriber = undefined;
            let timeout = setTimeout(() => {
                unsubscribe();
                reject(new RequestError(404, "Timeout on loading google api"));
            }, 10000);
            if(get(google_ready)) {
                clearTimeout(timeout);
                resolve(this.adjustInfo(LocationModel.getInstance().getInfo(this.#id, document.getElementById("location"))));
            } else {
                unsubscribe = google_ready.subscribe(_ready => {
                    if(_ready) {
                        unsubscribe();
                        clearTimeout(timeout);
                        resolve(this.adjustInfo(LocationModel.getInstance().getInfo(this.#id, document.getElementById("location"))));
                    }
                });
            }
        }));
    }

    async adjustInfo(info: Promise<Info>) : Promise<Info> {
        let _info: Info = await info;
        _info.name = capitalizeFirstLetter(_info.name);
        _info.address = capitalizeFirstLetter(_info.address);
        if(_info.types.length) {
            _info.types.forEach((value, index, array) => {array[index] = value.replaceAll('_', ' ')});
            _info.types.splice(_info.types.findIndex(value => value==='point of interest'), 1);
            _info.types.splice(_info.types.findIndex(value => value==='establishment'), 1);
        }
        return _info;
    }
}