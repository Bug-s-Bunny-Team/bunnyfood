import { ProfilesModel } from "../models/profilesModel";
import { AccountModel } from "../models/accountModel";
import type { Account, SocialProfile } from "../models";
import { writable, Writable } from "svelte/store";

export class FolloweesPresenter {

    profiles: Writable<Promise<SocialProfile[]>> = writable(null);
    disableButtons: Writable<boolean> = writable(false);

    constructor() {
        this.refresh = this.refresh.bind(this);
        this.removeFollowee = this.removeFollowee.bind(this);
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
        ProfilesModel.getInstance().removeFollowee(followee).finally(this.refresh);
    }
}
