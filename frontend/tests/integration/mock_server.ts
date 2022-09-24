import type { AxiosResponse } from 'axios'
import Locations from '../../mock/locations.json'
import Followed from '../../mock/followed.json'
import Profiles from '../../mock/social_profiles.json'
import PopularProfiles from '../../mock/popular_profiles.json'
import Preference from '../../mock/preferences.json'

export async function getResponse(url: string, options: RequestInit, params: any, query: any, fake_delay=false) : Promise<AxiosResponse<any>> {
    let res: any = {};
    const body = options.body ? JSON.parse(options.body.toString()) : undefined;
    if(fake_delay) await new Promise(r => {setTimeout(() => { r(undefined) }, 200)});
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
            switch(res.data ? res.data.id : undefined) {
                case 1: res.status=404; res.statusText='Not Found'; res.data = { detail: "" }; break;
                case undefined: res.status=404; res.statusText='Not Found'; res.data = { detail: "" }; break;
                default: res.status = 200; break;
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
            switch(res.data ? res.data.id : undefined) {
                case 1: res.status = 404; res.statusText='Not Found'; res.data = { detail: "" }; break;
                case undefined: res.status=404; res.statusText='Not Found'; res.data = { detail: "" }; break;
                default: res.status = 200; break;
            }
            return res;

        case 'GET /api/profiles/search/{profile_username}':
            res.data = Profiles;
            res.statusText = 'OK';
            res.data = res.data.find((profile: any) => { return profile.username == params.profile_username });
            switch(res.data ? res.data.id : undefined) {                    
                case 1: res.status = 201; break;

                case 2: res.status = 204; res.data = undefined; break;

                case 3: res.status = 404; res.statusText='Not Found'; res.data = { detail: "" }; break;

                case undefined: res.status=404; res.statusText='Not Found'; res.data = { detail: "" }; break;

                default: res.status = 200; break;
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
            switch(follow_profile ? follow_profile.id : undefined) {
                case 1: res.status = 404; res.statusText='Not Found'; res.data = { detail: "" }; break;

                case undefined: res.status=404; res.statusText='Not Found'; res.data = { detail: "" }; break;

                default: res.status = 201; res.data = follow_profile; break;
            }
            return res;

        case 'POST /api/followed/unfollow/':
            res.data = Followed;
            res.statusText = 'OK';
            const unfollow_profile = res.data.find((profile: any) => {return profile.username == body.username});
            switch(unfollow_profile ? unfollow_profile.id : undefined) {
                case 1: res.status = 404; res.statusText='Not Found'; res.data = { detail: "" }; break;

                case undefined: res.status=404; res.statusText='Not Found'; res.data = { detail: "" }; break;

                default: res.status = 200; res.data = unfollow_profile; break;
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

export function formatUrl(url: string, config: RequestInit) : {method: string, path: string, params: any, query: any} {
    let params: any = {};
    let query: any = {};
    if(url.match(/\/api\/profiles\/search\/.*/)) {
        params.profile_username = url.split('/api/profiles/search/')[1];
        url = '/api/profiles/search/{profile_username}';
    } else if(url.match(/\/api\/profiles\/popular\/.*/)) {
        params.limit = JSON.parse(url.split('/api/profiles/popular/')[1]);
        url = '/api/profiles/popular/{limit}';
    } else if(url.match(/\/api\/profiles\/.+/)) {
        params.profile_id = JSON.parse(url.split('/api/profiles/')[1]);
        url = '/api/profiles/{profile_id}';
    } else if(url.match(/\/api\/locations\/?.+/)) {
        const params = Object.fromEntries(new URL(`${window.location.protocol}//${window.location.hostname}` + url).searchParams.entries());
        url = '/api/locations/';
    } else if(url.match(/\/api\/locations\/.+/)) {
        params.location_id = JSON.parse(url.split('/api/locations/')[1]);
        url = '/api/locations/{location_id}';
    }

    return {method: config.method as string, path: url, params: params, query: query}
}

export async function mock_fetch(url: RequestInfo | URL, options?: RequestInit) : Promise<any> {
    url = url.toString();
    const formattedRequest = formatUrl(url, options as RequestInit);
    const res = await getResponse(formattedRequest.path, options as RequestInit, formattedRequest.params, formattedRequest.query, true);

    return {
        ok: (200<=res.status && res.status<=299),
        status: res.status,
        statusText: res.statusText,
        json: () => res.data
    };
}