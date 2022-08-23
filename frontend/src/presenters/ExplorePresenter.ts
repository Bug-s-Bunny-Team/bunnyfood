import type { RequestError, SocialProfile } from "../models";
import { writable, Writable } from "svelte/store";
import { ProfilesModel } from "../models/profilesModel";
import ErrorSvelte from "../components/Error.svelte";

export class ExplorePresenter {

    profiles: Writable<Promise<SocialProfile[]>> = writable(null);
    disableButtons: Writable<boolean> = writable(false);

    constructor() {
        this.refresh = this.refresh.bind(this);
        this.addProfile = this.addProfile.bind(this);
        this.refresh();
    }

    refresh() : void {
        this.disableButtons.set(true);
        let promise = ProfilesModel.getInstance().getMostPopularProfiles(20);
        promise.finally(() => {this.disableButtons.set(false)});
        this.profiles.set(promise);
    }

    addProfile(profile: SocialProfile) : void {
        this.disableButtons.set(true);
        ProfilesModel.getInstance().followProfile(profile).catch((e: RequestError) => {new ErrorSvelte({props: {error: e}, target: document.getElementById('error')})}).finally(this.refresh);
    }
}
