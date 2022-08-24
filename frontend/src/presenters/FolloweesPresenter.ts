import { ProfilesModel } from "../models/profilesModel";
import type { RequestError, SocialProfile } from "../models";
import { writable, Writable } from "svelte/store";
import ErrorSvelte from "../components/Error.svelte";
import { error_duration, removeChildren } from "../utils";

export class FolloweesPresenter {

    profiles: Writable<Promise<SocialProfile[]>> = writable(null);
    disableButtons: Writable<boolean> = writable(false);
    errorTimeout: NodeJS.Timeout = null;

    constructor() {
        this.refresh = this.refresh.bind(this);
        this.removeFollowee = this.removeFollowee.bind(this);
        this.destroy = this.destroy.bind(this);
        this.refresh();
    }

    refresh() : void {
        this.disableButtons.set(true);
        let promise = ProfilesModel.getInstance().getFollowees();
        promise.finally(() => {this.disableButtons.set(false)});
        this.profiles.set(promise);    
    }

    removeFollowee(followee: SocialProfile) : void {
        this.disableButtons.set(true);
        ProfilesModel.getInstance().removeFollowee(followee)
            .catch((e: RequestError) => { 
                removeChildren(document.getElementById('error')); 
                const message = 'An error occurred, please try again';
                new ErrorSvelte({props: {message: message}, target: document.getElementById('error')});
                this.errorTimeout = setTimeout(() => {removeChildren(document.getElementById('error'))}, error_duration);
            })
            .finally(this.refresh);
    }

    destroy() {
        if(this.errorTimeout) clearTimeout(this.errorTimeout);
    }
}
