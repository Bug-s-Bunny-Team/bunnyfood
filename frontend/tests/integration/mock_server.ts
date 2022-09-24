import type { AxiosResponse } from 'axios'
import Locations from '../../mock/locations.json'
import Followed from '../../mock/followed.json'
import Profiles from '../../mock/social_profiles.json'
import PopularProfiles from '../../mock/popular_profiles.json'
import Preference from '../../mock/preferences.json'

export async function getResponse(url: string, options: RequestInit, params: any, query: any) : Promise<AxiosResponse<any>> {
    let res: any = {};
    const body = options.body ? JSON.parse(options.body.toString()) : undefined;
    switch((options.method as string).toUpperCase() + ' ' + url) {
        case 'GET /api/locations/':
            res.data = Locations;
            res.status = 200;
            res.statusText = 'OK';
            return res;
            
        case 'GET /api/locations/{location_id}':
            res.data = Locations;
            res.status = 200;
            res.statusText = 'OK'
            res.data = res.data.find((location: any) => { return location.id == params.location_id });
            switch(res.data.id) {
                case 0: res.status=200; break;
                case 1: res.status=404; res.statusText='Not Found'; res.data = { detail: "" }; break;
            }
            return res;
        
        case 'GET /api/profiles/':
            res.data = Profiles;
            res.status = 200;
            res.statusText = 'OK';
            return res;

        case 'GET /api/profiles/{profile_id}':
            res.data = Profiles;
            res.status = 200;
            res.statusText = 'OK';
            res.data = res.data.find((profile: any) => { return profile.id == params.profile_id });
            switch(res.data.id) {
                case 0: res.status = 200; break;
                    
                case 1: res.status = 404; res.statusText='Not Found'; res.data = { detail: "" }; break;
            }
            return res;

        case 'GET /api/profiles/search/{profile_username}':
            res.data = Profiles;
            res.statusText = 'OK';
            res.data = res.data.find((profile: any) => { return profile.username == params.profile_username });
            switch(res.data.id) {
                case 0: res.status = 200; break;
                    
                case 1: res.status = 201; break;

                case 2: res.status = 204; res.data = undefined; break;

                case 3: res.status = 404; res.statusText='Not Found'; res.data = { detail: "" }; break;
            }
            return res;
        
        case 'GET /api/profiles/popular/{limit}':
            res.data = PopularProfiles;
            res.status = 200;
            res.statusText = 'OK';
            return res;

        case 'GET /api/followed/':
            res.data = Followed;
            res.status = 200;
            res.statusText = 'OK';
            return res;

        case 'POST /api/followed/':
            res.data = Profiles;
            res.statusText = 'OK';
            const follow_profile = res.data.find((profile: any) => {return profile.username == body.username});
            switch(follow_profile.id) {
                case 0: res.status = 201; res.data = follow_profile; break;

                case 1: res.status = 404; res.statusText='Not Found'; res.data = { detail: "" }; break;
            }
            return res;

        case 'POST /api/followed/unfollow/':
            res.data = Followed;
            res.statusText = 'OK';
            const unfollow_profile = res.data.find((profile: any) => {return profile.username == body.username});
            switch(unfollow_profile.id) {
                case 0: res.status = 200; res.data = unfollow_profile; break;

                case 1: res.status = 404; res.statusText='Not Found'; res.data = { detail: "" }; break;
            }
            return res;
        
        case 'GET /api/preferences/':
            res.data = Preference;
            res.status = 200;
            res.statusText = 'OK';
            return res;

        case 'PUT /api/preferences/':
            res.data = Preference;
            res.status = 200;
            res.statusText = 'OK';
            return res;

        default: throw new Error('Invalid path');
    }
}