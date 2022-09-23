import { init, fetch } from '../../integration/integration'
import { expect, test, beforeAll, describe } from '@jest/globals'
import { ProfilesModel } from '../../../src/models/profilesModel'
import { RequestError, SocialProfile } from '../../../src/models';

beforeAll(async () => {
    await init();
    window.fetch = fetch;
})

const profiles_search_cases = [
    { username: 'antoniorazzi', validobj: true, throws: false },
    { username: 'tulliovardanega', validobj: true, throws: false },
    { username: 'cardin', validobj: false, obj: undefined, throws: false },
    { username: 'sergiomattarella', validobj: false, obj: null, throws: false },
]

describe('TUF10', () => {
    describe.each(profiles_search_cases)('1 - getProfile', test_case => {
        test('integration', async () => {
            try { await ProfilesModel.getInstance().getProfile(test_case.username) } 
            catch (e) { if(!(await RequestError.schema.isValid({code: e.code, message: e.message}))) throw e; }
        })
        test('function', async () => {
            const { username, validobj, throws } = test_case;
            let promise = ProfilesModel.getInstance().getProfile(username);
            
            await expect(promise).resolves.not.toThrow();
            //else await expect(promise).rejects.toBeInstanceOf(RequestError);
            
            if(validobj) await SocialProfile.schema.validate(await promise); 
            else expect(await promise).toStrictEqual(test_case.obj);
        })
    })

    describe('2 - getFollowed', () => {
        test('integration', async () => {
            try { await ProfilesModel.getInstance().getFollowed() } 
            catch (e) { if(!(await RequestError.schema.isValid({code: e.code, message: e.message}))) throw e; }
        })
        test('function', async () => {
            let promise = ProfilesModel.getInstance().getFollowed();
            
            await expect(promise).resolves.not.toThrow();
            
            let profiles = await promise;
            expect(profiles.length).toBeGreaterThan(0);
            await Promise.all(profiles.map(async profile => {
                await SocialProfile.schema.validate(profile); 
            }));
        })
    })
})