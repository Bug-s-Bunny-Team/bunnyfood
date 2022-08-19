import type { Account, SocialProfile } from '../models'

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
        const response = await fetch('dev-api/profiles');
        return await response.json();
    }

    async removeFollowee(profile: SocialProfile) : Promise<void> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
    }

    async getMostPopularProfiles(quantity: number) : Promise<SocialProfile[]> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        const response = await fetch('dev-api/profiles');
        return await response.json();
    }

    async getProfiles(ricerca: String) : Promise<SocialProfile[]> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
        const response = await fetch('dev-api/profiles');
        return await response.json();
    }

    async followProfile(profile: SocialProfile) : Promise<void> {
        await new Promise(r => setTimeout(r, ProfilesModel.static_delay_ms))
    }
}  
 
  