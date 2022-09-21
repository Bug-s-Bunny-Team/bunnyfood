import { jest, test, expect, beforeEach, describe } from '@jest/globals';
import { get } from 'svelte/store';
import { RequestError, SocialProfile } from '../../../src/models';
import { ProfilesModel } from '../../../src/models/profilesModel';
import { AddProfilesPresenter } from '../../../src/presenters/AddProfilesPresenter'
import { removeChildren } from '../../../src/utils';

jest.mock('../../../src/models/profilesModel');
ProfilesModel.getInstance().followProfile = jest.fn()   .mockResolvedValueOnce(undefined)
                                                        .mockRejectedValueOnce(new RequestError(400, "a"))
                                                        .mockRejectedValueOnce(new RequestError(400, "a"));

jest.useFakeTimers();

beforeEach(() => {
    removeChildren(document.getElementById('error'));
})

const test_username = "antoniorazzi";

describe('TUF8', () => {
    
    test('1 - search', async () => {
        let presenter = new AddProfilesPresenter();
        await get(presenter.profile);
        presenter.searchText.set(test_username);
    
        expect(get(presenter.disableButtons)).toStrictEqual(false);
        presenter.search();
        expect(get(presenter.disableButtons)).toStrictEqual(true);
    
        const profiles_prom = get(presenter.profile);
        expect(profiles_prom).toBeTruthy();
        const profile = await profiles_prom;
        expect(get(presenter.disableButtons)).toStrictEqual(false);
    
        expect(SocialProfile.schema.isValid(profile)).toBeTruthy();
        expect(profile.username).toStrictEqual(test_username);
    })

    describe('2 - addProfile', () => {
        test('noexcept', async () => {
            let presenter = new AddProfilesPresenter();
            presenter.searchText.set(test_username);
            presenter.search();

            const profile = await get(presenter.profile)
        
            let promise = presenter.addProfile(profile);
            expect(ProfilesModel.getInstance().followProfile).toHaveBeenCalledWith(profile);
            expect(get(presenter.disableButtons)).toStrictEqual(true);
            
            await expect(promise).resolves.toStrictEqual(undefined);
            expect(document.getElementById('error').childElementCount).toStrictEqual(0); // no errors
            expect(get(presenter.searchText)).toStrictEqual('');
            expect(get(presenter.profile)).toStrictEqual(null);
            expect(get(presenter.disableButtons)).toStrictEqual(false);
            expect(jest.getTimerCount()).toStrictEqual(0);
        })

        test('exception', async () => {
            let presenter = new AddProfilesPresenter();
            presenter.searchText.set(test_username);
            presenter.search();

            const profile = await get(presenter.profile)
        
            let promise = presenter.addProfile(profile);
            expect(ProfilesModel.getInstance().followProfile).toHaveBeenCalledWith(profile);
            expect(get(presenter.disableButtons)).toStrictEqual(true);
            
            await expect(promise).resolves.toStrictEqual(undefined);
            expect(document.getElementById('error').childElementCount).toStrictEqual(1); // one error
            expect(get(presenter.searchText)).toStrictEqual('');
            expect(get(presenter.profile)).toStrictEqual(null);
            expect(get(presenter.disableButtons)).toStrictEqual(false);
            expect(jest.getTimerCount()).toStrictEqual(1);

            jest.runAllTimers();

            expect(jest.getTimerCount()).toStrictEqual(0);
            expect(document.getElementById('error').childElementCount).toStrictEqual(0); // error removed
        })
    })

    describe('3 - destroy', () => {
        test('running timer', async () => {
            let presenter = new AddProfilesPresenter();
            presenter.searchText.set(test_username);
            presenter.search();

            const profile = await get(presenter.profile)
            await presenter.addProfile(profile);
            expect(jest.getTimerCount()).toStrictEqual(1);
            expect(document.getElementById('error').childElementCount).toStrictEqual(1); // one error
            
            presenter.destroy();
            
            expect(jest.getTimerCount()).toStrictEqual(0);
            expect(document.getElementById('error').childElementCount).toStrictEqual(0); // error removed
        })

        test('no running timer', () => {
            let presenter = new AddProfilesPresenter();
            presenter.destroy();
            
            expect(jest.getTimerCount()).toStrictEqual(0);
            expect(document.getElementById('error').childElementCount).toStrictEqual(0); // error removed
        })
    })
})