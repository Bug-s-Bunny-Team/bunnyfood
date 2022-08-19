import { ProfilesModel } from "../models/profilesModel";
import { Writable, writable } from "svelte/store";
import type { SocialProfile } from "src/models";


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
        ProfilesModel.getInstance().followProfile(profile).then(this.search);
    }
}
