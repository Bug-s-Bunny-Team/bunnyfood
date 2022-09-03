import { jest, test, describe, expect, beforeEach } from '@jest/globals';
import { get } from 'svelte/store';
import { RequestError } from '../../../src/models';
import { LocationPresenter } from '../../../src/presenters/LocationPresenter'
import { google_ready } from '../../../src/store';

jest.mock('../../../src/models/locationModel');
jest.useFakeTimers();

beforeEach(() => {
    jest.clearAllMocks();
    jest.clearAllTimers();
})

describe('TUF4', () => {
    test('1 - constructor', () => {
        const tmp = LocationPresenter.prototype.getInfo;
        LocationPresenter.prototype.getInfo = jest.fn();
        
        new LocationPresenter(0);
        expect(LocationPresenter.prototype.getInfo).toHaveBeenCalledTimes(1);
    
        LocationPresenter.prototype.getInfo = tmp;
    })
    
    describe('2 - get info', () => {
        test('google api ready', async () => {
            google_ready.set(true);
            const presenter = new LocationPresenter(0);
    
            const info = await get(presenter.info);
            expect(info).toBeTruthy();
            expect(info.address).toBeTruthy();
            expect(info.img).toBeTruthy();
            if(!info.img.alt) {
                expect(info.img.height).toBeTruthy();
                expect(info.img.width).toBeTruthy();
                expect(info.img.url).toBeTruthy();
                expect(info.img.alt).toEqual("");
            }
            expect(info.name).toBeTruthy();
            expect(info.score).not.toStrictEqual(undefined);
            expect(info.phone_number).toBeTruthy();
            expect(info.website).toBeTruthy();
            expect(info.types).toBeTruthy();
            expect(info.types).not.toContain("establishment");
            expect(info.types).not.toContain("point of interest");
    
            expect(info.name.charAt(0) == info.name.charAt(0).toUpperCase()).toBeTruthy();
            expect(info.address.charAt(0) == info.address.charAt(0).toUpperCase()).toBeTruthy();
        })
    
        test('google api not ready', () => {
            google_ready.set(false);
            const presenter = new LocationPresenter(0);
            expect(presenter.info).toBeTruthy();
            expect(jest.runAllTimers).toThrow(new RequestError(404, "Timeout on loading google api"));
        })
    });
    
})
