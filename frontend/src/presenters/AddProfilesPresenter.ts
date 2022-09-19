import type { RequestError, SocialProfile } from "../models";
import { ProfilesModel } from "../models/profilesModel";
import { get, Writable, writable } from "svelte/store";
import { error_duration, removeChildren } from "../utils";
import ErrorSvelte from "../components/Error.svelte";

export class AddProfilesPresenter {

    #searchText: Writable<string> = writable('');
    #profile: Writable<Promise<SocialProfile | null | undefined>> = writable(null);
    #disableButtons: Writable<boolean> = writable(false);
    #errorTimeout: NodeJS.Timeout = null;

    get searchText() { return this.#searchText }
    get profile() { return this.#profile }
    get disableButtons() { return this.#disableButtons }

    constructor() {
        this.search = this.search.bind(this);
        this.addProfile = this.addProfile.bind(this);
        this.destroy = this.destroy.bind(this);
    }

    search() : void {
        this.#disableButtons.set(true);
        let promise = ProfilesModel.getInstance().getProfile(get(this.#searchText));
        promise.finally(() => {this.#disableButtons.set(false)});
        this.#profile.set(promise);
    }

    addProfile(profile: SocialProfile) : void {
        this.#disableButtons.set(true);
        ProfilesModel.getInstance().followProfile(profile)
            .catch((e: RequestError) => { 
                removeChildren(document.getElementById('error')); 
                const message = 'An error occurred, please try again';
                new ErrorSvelte({props: {message: message}, target: document.getElementById('error')});
                this.#errorTimeout = setTimeout(() => {removeChildren(document.getElementById('error'))}, error_duration);
            })
            .finally(() => {
                this.#searchText.set('');
                this.#profile.set(null);
                this.#disableButtons.set(false);
            });
    }

    destroy() {
        if(this.#errorTimeout) clearTimeout(this.#errorTimeout);
    }
}
