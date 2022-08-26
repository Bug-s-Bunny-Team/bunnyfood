import { RequestError, SocialProfile } from '../models'
import { AccountModel } from './accountModel';

export class ProfilesModel {
    private static profilesModelInstance : ProfilesModel = ProfilesModel.construct_session();

    private static construct_session() : ProfilesModel {
        let result = new ProfilesModel();
        return result;
    }

    static getInstance() : ProfilesModel {
        return this.profilesModelInstance;
    }

    private constructor() { 
    }

    private static static_delay_ms = 200;

    async getFollowees() {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const response = await fetch('api/followed/', AccountModel.getInstance().getRequestOptions());
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }

    async removeFollowee(profile: SocialProfile) : Promise<void> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const options = AccountModel.getInstance().postRequestOptions();
        options.body = JSON.stringify({username: profile.username});
        const response = await fetch('api/followed/unfollow', options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }

    async getMostPopularProfiles(quantity: number = 20) : Promise<SocialProfile[]> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const response = await fetch(`api/profiles/popular/${quantity}`, AccountModel.getInstance().getRequestOptions());
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }

    async getProfiles(ricerca: string) : Promise<SocialProfile[]> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const url = new URL('api/profiles/', `${window.location.protocol}//${window.location.host}`);
        url.searchParams.append('username', encodeURIComponent(ricerca));
        const response = await fetch(url, AccountModel.getInstance().getRequestOptions());
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }

    async followProfile(profile: SocialProfile) : Promise<void> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const options = AccountModel.getInstance().postRequestOptions();
        options.body = JSON.stringify({username: profile.username});
        const response = await fetch('api/followed/', options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }
}  
 
  