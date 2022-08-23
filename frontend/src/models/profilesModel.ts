import { Account, RequestError, SocialProfile } from '../models'

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

    static get_request_options: RequestInit = {
        method: 'GET',
        mode: 'same-origin',
        credentials: 'same-origin'
    };

    static post_request_options: RequestInit = {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
        },
        body: ""
    };

    private static static_delay_ms = 200;

    async getFollowees() {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const response = await fetch('dev-api/followed', ProfilesModel.get_request_options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }

    async removeFollowee(profile: SocialProfile) : Promise<void> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const options = ProfilesModel.post_request_options;
        options.body = JSON.stringify({username: profile.username});
        const response = await fetch('dev-api/followed/unfollow', options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }

    async getMostPopularProfiles(quantity: number = 20) : Promise<SocialProfile[]> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const response = await fetch(`dev-api/profiles/popular/${quantity}`, ProfilesModel.get_request_options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }

    async getProfiles(ricerca: String) : Promise<SocialProfile[]> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const response = await fetch('dev-api/profiles'); // TODO
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }

    async followProfile(profile: SocialProfile) : Promise<void> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        
        const options = ProfilesModel.post_request_options;
        options.body = JSON.stringify({username: profile.username});
        const response = await fetch('dev-api/followed', options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(res.code, res.msg);
        return res;
    }
}  
 
  