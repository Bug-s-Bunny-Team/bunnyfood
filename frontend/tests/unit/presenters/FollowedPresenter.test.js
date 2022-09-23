import { jest, test, expect, beforeEach, describe } from '@jest/globals';
import { get } from 'svelte/store';
import { RequestError, SocialProfile } from '../../../src/models';
import { ProfilesModel } from '../../../src/models/profilesModel';
import { FollowedPresenter } from '../../../src/presenters/FollowedPresenter'
import { removeChildren } from '../../../src/utils';

jest.mock('../../../src/models/profilesModel');
ProfilesModel.getInstance().removeFollowed = jest.fn()  .mockResolvedValueOnce(undefined)
                                                        .mockRejectedValueOnce(new RequestError(400, "a"))
                                                        .mockRejectedValueOnce(new RequestError(400, "a"));

jest.useFakeTimers();

beforeEach(() => {
    removeChildren(document.getElementById('error'));
    jest.clearAllMocks();
})

describe('TUF8', () => {
    test('1 - constructor', () => {
        const tmp = FollowedPresenter.prototype.refresh;
        FollowedPresenter.prototype.refresh = jest.fn();
        
        new FollowedPresenter();
        expect(FollowedPresenter.prototype.refresh).toHaveBeenCalledTimes(1);
        
        FollowedPresenter.prototype.refresh = tmp;
    })
    
    test('2 - refresh', async () => {
        let presenter = new FollowedPresenter();
        await get(presenter.profiles);
        expect(ProfilesModel.getInstance().getFollowed).toHaveBeenCalledTimes(1);
    
        expect(get(presenter.disableButtons)).toStrictEqual(false);
        presenter.refresh();
        expect(get(presenter.disableButtons)).toStrictEqual(true);
    
        const profiles_prom = get(presenter.profiles);
        expect(profiles_prom).toBeTruthy();
        await profiles_prom;
        expect(get(presenter.disableButtons)).toStrictEqual(false);
        expect(ProfilesModel.getInstance().getFollowed).toHaveBeenCalledTimes(2);
    })

    describe('3 - removeFollowed', () => {
        test('noexcept', async () => {
            let presenter = new FollowedPresenter();
            presenter.refresh = jest.fn();

            const list = await get(presenter.profiles)
        
            let promise = presenter.removeFollowed(list[0]);
            expect(ProfilesModel.getInstance().removeFollowed).toHaveBeenCalledTimes(1);
            expect(ProfilesModel.getInstance().removeFollowed).toHaveBeenLastCalledWith(list[0]);
            expect(get(presenter.disableButtons)).toStrictEqual(true);
            expect(presenter.refresh).not.toHaveBeenCalled();
            
            await expect(promise).resolves.toStrictEqual(undefined);
            expect(document.getElementById('error').childElementCount).toStrictEqual(0); // no errors
            expect(presenter.refresh).toHaveBeenCalledTimes(1); // successfully finished promise
            expect(jest.getTimerCount()).toStrictEqual(0);
        })

        test('exception', async () => {
            let presenter = new FollowedPresenter();
            presenter.refresh = jest.fn();
    
            const list = await get(presenter.profiles)
            
            let promise = presenter.removeFollowed(list[0]);
            expect(ProfilesModel.getInstance().removeFollowed).toHaveBeenCalledTimes(1);
            expect(ProfilesModel.getInstance().removeFollowed).toHaveBeenLastCalledWith(list[0]);
            expect(get(presenter.disableButtons)).toStrictEqual(true);
            expect(presenter.refresh).not.toHaveBeenCalled();
            
            await expect(promise).resolves.toStrictEqual(undefined);
            expect(document.getElementById('error').childElementCount).toStrictEqual(1); // one error
            expect(presenter.refresh).toHaveBeenCalledTimes(1); // successfully finished promise
            expect(jest.getTimerCount()).toStrictEqual(1);

            jest.runAllTimers();

            expect(jest.getTimerCount()).toStrictEqual(0);
            expect(document.getElementById('error').childElementCount).toStrictEqual(0); // error removed
        })
    })

    describe('4 - destroy', () => {
        test('running timer', async () => {
            let presenter = new FollowedPresenter();
            presenter.refresh = jest.fn();
    
            const list = await get(presenter.profiles)
            await presenter.removeFollowed(list[0]);
            expect(jest.getTimerCount()).toStrictEqual(1);
            expect(document.getElementById('error').childElementCount).toStrictEqual(1); // one error
            
            presenter.destroy();
            
            expect(jest.getTimerCount()).toStrictEqual(0);
            expect(document.getElementById('error').childElementCount).toStrictEqual(0); // error removed
        })

        test('no running timer', () => {
            let presenter = new FollowedPresenter();
            presenter.destroy();
            
            expect(jest.getTimerCount()).toStrictEqual(0);
            expect(document.getElementById('error').childElementCount).toStrictEqual(0); // error removed
        })
    })
})