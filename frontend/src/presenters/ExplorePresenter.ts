import type { RequestError, SocialProfile } from "../models";
import { writable, Writable } from "svelte/store";
import { ProfilesModel } from "../models/profilesModel";
import { error_duration, removeChildren } from "../utils";
import ErrorSvelte from "../components/Error.svelte";

export class ExplorePresenter {

    #profiles: Writable<Promise<SocialProfile[]>> = writable(null);
    #disableButtons: Writable<boolean> = writable(false);
    #errorTimeout: NodeJS.Timeout = null;

    get profiles() { return this.#profiles }
    get disableButtons() { return this.#disableButtons }

    constructor() {
        this.refresh = this.refresh.bind(this);
        this.addProfile = this.addProfile.bind(this);
        this.destroy = this.destroy.bind(this);
        this.refresh();
    }

    refresh() : void {
        this.#disableButtons.set(true);
        let promise = ProfilesModel.getInstance().getMostPopularProfiles(20);
        promise.finally(() => {this.#disableButtons.set(false)});
        this.profiles.set(promise);
    }

    async addProfile(profile: SocialProfile) : Promise<void> {
        this.#disableButtons.set(true);
        return ProfilesModel.getInstance().followProfile(profile)
            .catch((e: RequestError) => { 
                removeChildren(document.getElementById('error')); 
                const message = 'An error occurred, please try again';
                new ErrorSvelte({props: {message: message}, target: document.getElementById('error')});
                this.#errorTimeout = setTimeout(() => {removeChildren(document.getElementById('error'))}, error_duration);
            })
            .finally(this.refresh);
    }

    destroy() {
        if(this.#errorTimeout) {
          removeChildren(document.getElementById('error'));
          clearTimeout(this.#errorTimeout)
        } 
    }
}
