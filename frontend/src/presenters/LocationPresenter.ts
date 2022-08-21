import type { Info } from "../models";
import { LocationModel } from "../models/locationModel";
import { get, Writable, writable } from "svelte/store";
import { google_ready } from "../store";

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
            this.info.set(this.adjustInfo(LocationModel.getInstance().getInfo(this.#id)));
        }
        else {
            this.info.set(new Promise(async resolve => {
                let resolved = false;
                google_ready.subscribe(_ready => {
                    if(_ready) {
                        resolved = true;
                        resolve(this.adjustInfo(LocationModel.getInstance().getInfo(this.#id)));
                    }
                });
                await new Promise(r => setTimeout(r, 10000));
                if(!resolved) throw new Error("Couldn't load google api.");
            }));
        }
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