import { ProfilesModel } from "../models/profilesModel";
import { Writable, writable } from "svelte/store";
import type { RequestError, SocialProfile } from "../models";
import ErrorSvelte from "../components/Error.svelte";


export class AddProfilesPresenter {

    searchText: string;
    profiles: Writable<Promise<SocialProfile[]>> = writable(null);
    disableButtons: Writable<boolean> = writable(false);

    constructor() {
        this.search = this.search.bind(this);
        this.addProfile = this.addProfile.bind(this);
    }

    search() : void {
        this.disableButtons.set(true);
        let promise = ProfilesModel.getInstance().getProfiles(this.searchText);
        promise.finally(() => {this.disableButtons.set(false)});
        this.profiles.set(promise);
    }

    addProfile(profile: SocialProfile) : void {
        this.disableButtons.set(true);
        ProfilesModel.getInstance().followProfile(profile).catch((e: RequestError) => {new ErrorSvelte({props: {error: e}, target: document.getElementById('error')})}).finally(this.search);
    }
}
