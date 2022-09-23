import { AxiosResponse } from 'axios'
import axios from 'axios'

export async function getResponse(url: string, options: RequestInit, params: any, query: any) : Promise<AxiosResponse<any>> {
    let res: any = {};
    let _res: any;
    const body = options.body ? JSON.parse(options.body.toString()) : undefined;
    switch((options.method as string).toUpperCase() + ' ' + url) {
        case 'GET /api/locations/':
            return await axios.get('http://localhost:5000/mock/locations.json');
            
        case 'GET /api/locations/{location_id}':
            res = await axios.get('http://localhost:5000/mock/locations.json');
            res.data = res.data.find((location: any) => { return location.id == params.location_id });
            switch(res.data.id) {
                case 0: res.status=200; break;
                case 1: res.status=404; res.data = { detail: "" }; break;
            }
            return res;
        
        case 'GET /api/profiles/':
            return await axios.get('http://localhost:5000/mock/followed.json');

        case 'GET /api/profiles/{profile_id}':
            res = await axios.get('http://localhost:5000/mock/followed.json');
            res.data = res.data.find((profile: any) => { return profile.id == params.profile_id });
            switch(res.data.id) {
                case 0: res.status = 200; break;
                    
                case 1: res.status = 404; res.data = { detail: "" }; break;
            }
            return res;

        case 'GET /api/profiles/search/{profile_username}':
            res = await axios.get('http://localhost:5000/mock/followed.json');
            res.data = res.data.find((profile: any) => { return profile.username == params.profile_username });
            switch(res.data.id) {
                case 0: res.status = 200; break;
                    
                case 1: res.status = 201; break;

                case 2: res.status = 204; res.data = undefined; break;

                case 3: res.status = 404; res.data = { detail: "" }; break;
            }
            return res;
        
        case 'GET /api/profiles/popular/{limit}':
            res = await axios.get('http://localhost:5000/mock/popular_profiles.json');
            switch(res.data.id) {
                case 0: res.status = 200; break;

                case 1: res.status = 400; res.data = { detail: "" }; break;
            }
            return res;

        case 'GET /api/followed/':
           return await axios.get('http://localhost:5000/mock/followed.json');

        case 'POST /api/followed/':
            _res =  await axios.get('http://localhost:5000/mock/followed.json');
            const follow_profile = _res.data.find((profile: any) => {return profile.username == body.username});
            switch(follow_profile.id) {
                case 0: res.status = 201; res.data = follow_profile; break;

                case 1: res.status = 404; res.data = { detail: "" }; break;
            }
            return res;

        case 'POST /api/followed/unfollow/':
            _res = await axios.get('http://localhost:5000/mock/followed.json');
            const unfollow_profile = _res.data.find((profile: any) => {return profile.username == body.username});
            switch(unfollow_profile.id) {
                case 0: res.status = 200; res.data = unfollow_profile; break;

                case 1: res.status = 404; res.data = { detail: "" }; break;
            }
            return res;
        
        case 'GET /api/preferences/':
            return await axios.get('http://localhost:5000/mock/preferences.json');

        case 'PUT /api/preferences/':
            return await axios.get('http://localhost:5000/mock/preferences.json');

        default: throw new Error('Invalid path');
    }
}