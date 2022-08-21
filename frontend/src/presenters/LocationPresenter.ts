import type { Info } from "../models";
import { LocationModel } from "../models/locationModel";
import { get, Writable, writable } from "svelte/store";
import { google_ready } from "../store";
import { capitalizeFirstLetter } from "../utils";

export class LocationPresenter {
    #id: number;
    info: Writable<Promise<Info>> = writable();

    constructor(id: number) {
        this.#id = id;
        this.getInfo = this.getInfo.bind(this);
        this.getInfo();
    }

    getInfo() : void {
        if(get(google_ready)) {
            this.info.set(this.adjustInfo(LocationModel.getInstance().getInfo(this.#id, document.getElementById("location"))));
        }
        else {
            this.info.set(new Promise(async resolve => {
                let resolved = false;
                google_ready.subscribe(_ready => {
                    if(_ready) {
                        resolved = true;
                        resolve(this.adjustInfo(LocationModel.getInstance().getInfo(this.#id, document.getElementById("location"))));
                    }
                });
                await new Promise(r => setTimeout(r, 10000));
                if(!resolved) throw new Error("Couldn't load google api.");
            }));
        }
    }

    async adjustInfo(info: Promise<Info>) : Promise<Info> {
        let _info: Info = await info;
        _info.name = capitalizeFirstLetter(_info.name);
        _info.address = capitalizeFirstLetter(_info.address);
        return _info;
    }
}