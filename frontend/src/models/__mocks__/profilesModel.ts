import { jest } from '@jest/globals'
import { RequestError, SocialProfile } from '../../models'
import Followed from '../../../mock/followed.json'
import Popular from '../../../mock/popular_profiles.json'
import Profiles from '../../../mock/social_profiles.json'

export class ProfilesModel {
    private static profilesModelInstance : ProfilesModel = ProfilesModel.construct_session();

    private static construct_session() : ProfilesModel {
        return new ProfilesModel();
    }

    static getInstance() : ProfilesModel {
        return this.profilesModelInstance;
    }

    private constructor() { 
    }

    async getFollowed() : Promise<SocialProfile[]> {
        return Followed;
    }

    removeFollowed = jest.fn();

    async getMostPopularProfiles(quantity: number = 20) : Promise<SocialProfile[]> {
        return Popular;
    }

    async getProfile(ricerca: string) : Promise<SocialProfile> {
        let profile: SocialProfile = Profiles.find((profile: SocialProfile) => profile.username==ricerca);
        if(profile) return profile;
        else throw new RequestError(404, "Profile not found");
    }

    followProfile = jest.fn();
}  
 
  