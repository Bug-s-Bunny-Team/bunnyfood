import type { RequestError, SocialProfile } from "../models";
import { ProfilesModel } from "../models/profilesModel";
import { Writable, writable } from "svelte/store";
import { error_duration, removeChildren } from "../utils";
import ErrorSvelte from "../components/Error.svelte";

export class AddProfilesPresenter {

    searchText: string;
    profile: Writable<Promise<SocialProfile>> = writable(null);
    disableButtons: Writable<boolean> = writable(false);
    errorTimeout: NodeJS.Timeout = null;

    constructor() {
        this.search = this.search.bind(this);
        this.addProfile = this.addProfile.bind(this);
        this.destroy = this.destroy.bind(this);
    }

    search() : void {
        this.disableButtons.set(true);
        let promise = ProfilesModel.getInstance().getProfile(this.searchText);
        promise.finally(() => {this.disableButtons.set(false)});
        this.profile.set(promise);
    }

    addProfile(profile: SocialProfile) : void {
        this.disableButtons.set(true);
        ProfilesModel.getInstance().followProfile(profile)
            .catch((e: RequestError) => { 
                removeChildren(document.getElementById('error')); 
                const message = 'An error occurred, please try again';
                new ErrorSvelte({props: {message: message}, target: document.getElementById('error')});
                this.errorTimeout = setTimeout(() => {removeChildren(document.getElementById('error'))}, error_duration);
            })
            .finally(this.search);
    }

    destroy() {
        if(this.errorTimeout) clearTimeout(this.errorTimeout);
    }
}
