import jestOpenAPI from 'jest-openapi';
import { expect } from '@jest/globals'

import toSatisfyApiSpec from 'jest-openapi/dist/matchers/toSatisfyApiSpec'
import toSatisfySchemaInApiSpec from 'jest-openapi/dist/matchers/toSatisfySchemaInApiSpec'
import axios from 'axios'
import http from 'axios/lib/adapters/http'
import OpenApiRequestValidator from 'openapi-request-validator'

import { getResponse, formatUrl } from './mock_server';

let openapi_spec: any;
let initialized = false;

function toValidatorRequest(url: string, config: RequestInit, params: any, query: any) : any {
    return {
        headers: config.headers,
        body: config.body ? JSON.parse((config.body as BodyInit).toString()) : {},
        params: params,
        query: query
    }
}

function createPathValidator(obj: {method: string, path: string, params: any}) : OpenApiRequestValidator {
    if(!(openapi_spec.paths[obj.path] && openapi_spec.paths[obj.path][obj.method.toLowerCase()])) throw new Error(`Path does not exist in API: ${obj.method+' '+obj.path}`) 
    
    let path = Object.assign({}, openapi_spec.paths[obj.path][obj.method.toLowerCase()]);
    path.schemas = Object.assign({}, openapi_spec.components.schemas);
    return new OpenApiRequestValidator(path);
}


async function test_init(test: boolean = false) {
    expect.extend({toSatisfyApiSpec,toSatisfySchemaInApiSpec}) 
    const res = await axios.get('https://d18v2wlpbu3jpw.cloudfront.net/api/openapi.json', {adapter: http});
    openapi_spec = res.data; 
    jestOpenAPI(res.data);
    initialized = true;
}

export async function test_fetch(url: RequestInfo | URL, options?: RequestInit) : Promise<any> {
    url = url.toString();
    if(!initialized) await test_init();

    const formattedRequest = formatUrl(url, options as RequestInit);
    const validatorRequest = toValidatorRequest(url, options as RequestInit, formattedRequest.params, formattedRequest.query);

    expect(createPathValidator(formattedRequest)
              .validateRequest(validatorRequest)).toBeFalsy();
    
    const res = await getResponse(formattedRequest.path, options as RequestInit, formattedRequest.params, formattedRequest.query, false);
    res.request = formattedRequest;
    expect(res).toSatisfyApiSpec();

    return {
        ok: (200<=res.status && res.status<=299),
        status: res.status,
        statusText: res.statusText,
        json: () => res.data
    };
}