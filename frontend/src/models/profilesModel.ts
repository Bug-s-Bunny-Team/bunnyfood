import { RequestError, SocialProfile } from '../models'
import { RequestOptions } from './requestOptions';

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

    async getFollowees() {        
        const response = await fetch('api/followed/', RequestOptions.getRequestOptions());
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(response.status, res.msg);
        return res;
    }

    async removeFollowee(profile: SocialProfile) : Promise<void> {        
        const options = RequestOptions.postRequestOptions();
        options.body = JSON.stringify({username: profile.username});
        const response = await fetch('api/followed/unfollow/', options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(response.status, res.msg);
        return res;
    }

    async getMostPopularProfiles(quantity: number = 20) : Promise<SocialProfile[]> {        
        const response = await fetch(`api/profiles/popular/${quantity}`, RequestOptions.getRequestOptions());
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(response.status, res.msg);
        return res;
    }

    async getProfiles(ricerca: string) : Promise<SocialProfile[]> {        
        const response = await fetch(`api/profiles/search/${encodeURIComponent(ricerca)}`, RequestOptions.getRequestOptions());
        
        const res = await response.json();
        if(!response.ok) {
            if(response.status == 404) return [];
            throw new RequestError(response.status, res.msg);
        }
        return res;
    }

    async followProfile(profile: SocialProfile) : Promise<void> {        
        const options = RequestOptions.postRequestOptions();
        options.body = JSON.stringify({username: profile.username});
        const response = await fetch('api/followed/', options);
        
        const res = await response.json();
        if(!response.ok) throw new RequestError(response.status, res.msg);
        return res;
    }
}  
 
  