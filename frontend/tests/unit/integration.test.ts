import jestOpenAPI from 'jest-openapi';
import { jest, describe, beforeAll, test, expect } from '@jest/globals'
import toSatisfyApiSpec from 'jest-openapi/dist/matchers/toSatisfyApiSpec'
import toSatisfySchemaInApiSpec from 'jest-openapi/dist/matchers/toSatisfySchemaInApiSpec'
import axios from 'axios'
import http from 'axios/lib/adapters/http'

expect.extend({toSatisfyApiSpec,toSatisfySchemaInApiSpec});

beforeAll(async () => {
    const res = await axios.get('https://d18v2wlpbu3jpw.cloudfront.net/api/openapi.json', {adapter: http});
    jestOpenAPI(res.data);
})

async function getFollowed() : Promise<any> {
    const res = await axios.get('http://localhost:5000/mock/followed.json');
    res.request = {method: 'GET', path: '/api/followed/'}
    return res;
}

test('/api/followed/', async () => {
    const res = await getFollowed();
    expect(res).toSatisfyApiSpec();
})




async function fetch(url: string, options: any) {
    let data;
    switch(url) {
        case '/api/followed/':
            data = getFollowed();
            break;
        
        // ...

        default: expect(0).toBeTruthy()
    }
    return {json: async () => (await data).data}
}