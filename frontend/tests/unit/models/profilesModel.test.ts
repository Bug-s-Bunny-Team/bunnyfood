import { init, fetch } from '../../integration/integration'
import { expect, test, beforeAll, describe, jest } from '@jest/globals'
import { ProfilesModel } from '../../../src/models/profilesModel'
import { RequestError, SocialProfile } from '../../../src/models';
import { AccountModel } from '../../../src/models/accountModel';

jest.mock('../../../src/models/accountModel')

beforeAll(async () => {
    await init();
    window.fetch = fetch;
    await AccountModel.getInstance().createAccount();
})

const profiles_search_cases = [
    { username: 'antoniorazzi', validobj: true, throws: false },
    { username: 'tulliovardanega', validobj: true, throws: false },
    { username: 'cardin', validobj: false, obj: undefined, throws: false },
    { username: 'sergiomattarella', validobj: false, obj: null, throws: false },
]

const follow_test_cases = [
    { profile: new SocialProfile(0, 'antoniorazzi'), throws: false },
    { profile: new SocialProfile(1, 'tulliovardanega'), throws: true }
]

describe('TUF10', () => {
    describe('1 - getFollowed', () => {
        test('integration', async () => {
            try { await ProfilesModel.getInstance().getFollowed() } 
            catch (e) { if(!(await RequestError.schema.isValid(e))) throw e; }
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

    describe.each(follow_test_cases)('2 - removeFollowed', test_case => {
        test('integration', async () => {
            try { await ProfilesModel.getInstance().removeFollowed(test_case.profile) } 
            catch (e) { if(!(await RequestError.schema.isValid(e))) throw e; }
        })
        test('function', async () => {
            const { profile, throws } = test_case;
            let promise = ProfilesModel.getInstance().removeFollowed(profile);
            
            if(!throws) await expect(promise).resolves.not.toThrow();
            else await expect(promise).rejects.toBeInstanceOf(RequestError);
        })
    })

    describe('3 - getMostPopularProfiles', () => {
        test('integration', async () => {
            try { await ProfilesModel.getInstance().getMostPopularProfiles() } 
            catch (e) { if(!(await RequestError.schema.isValid(e))) throw e; }
        })
        test('function', async () => {
            let promise = ProfilesModel.getInstance().getMostPopularProfiles();
            
            await expect(promise).resolves.not.toThrow();
            
            let profiles = await promise;
            expect(profiles.length).toBeGreaterThan(0);
            await Promise.all(profiles.map(async profile => {
                await SocialProfile.schema.validate(profile); 
            }));
        })
    })

    describe.each(profiles_search_cases)('4 - getProfile', test_case => {
        test('integration', async () => {
            try { await ProfilesModel.getInstance().getProfile(test_case.username) } 
            catch (e) { if(!(await RequestError.schema.isValid(e))) throw e; }
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

    describe.each(follow_test_cases)('5 - followProfile', test_case => {
        test('integration', async () => {
            try { await ProfilesModel.getInstance().followProfile(test_case.profile) } 
            catch (e) { if(!(await RequestError.schema.isValid(e))) throw e; }
        })
        test('function', async () => {
            const { profile, throws } = test_case;
            let promise = ProfilesModel.getInstance().followProfile(profile);
            
            if(!throws) await expect(promise).resolves.not.toThrow();
            else await expect(promise).rejects.toBeInstanceOf(RequestError);
        })
    })
})