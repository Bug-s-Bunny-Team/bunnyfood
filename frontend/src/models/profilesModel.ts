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

    async getFollowed() : Promise<SocialProfile[]> {        
        const response = await fetch('/api/followed/', RequestOptions.getRequestOptions());
        if(!response.ok) throw new RequestError(response.status, response.statusText);
        
        const res = await response.json();
        return res;
    }

    async removeFollowed(profile: SocialProfile) : Promise<void> {        
        const options = RequestOptions.postRequestOptions();
        options.body = JSON.stringify({username: profile.username});
        const response = await fetch('/api/followed/unfollow/', options);
        if(!response.ok) throw new RequestError(response.status, response.statusText);
        
        const res = await response.json();
        return res;
    }

    async getMostPopularProfiles(quantity: number = 20) : Promise<SocialProfile[]> {        
        const response = await fetch(`/api/profiles/popular/${quantity}`, RequestOptions.getRequestOptions());
        if(!response.ok) throw new RequestError(response.status, response.statusText);
        
        const res = await response.json();
        return res;
    }

    async getProfile(ricerca: string) : Promise<SocialProfile> {        
        const response = await fetch(`/api/profiles/search/${encodeURIComponent(ricerca)}`, RequestOptions.getRequestOptions());
        if(!response.ok) {
            if(response.status == 404) return null;
            throw new RequestError(response.status, response.statusText);
        }
        if(response.status==204) return undefined;
        const res = await response.json();
        return res;
    }

    async followProfile(profile: SocialProfile) : Promise<void> {        
        const options = RequestOptions.postRequestOptions();
        options.body = JSON.stringify({username: profile.username});
        const response = await fetch('/api/followed/', options);
        if(!response.ok) throw new RequestError(response.status, response.statusText);
    }
}  
 
  