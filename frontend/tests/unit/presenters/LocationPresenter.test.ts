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

let test_cases = [0, 1, 2, 3, 4, 5, 6];

describe.each(test_cases)('TUF4', id => {
    test('1 - constructor', () => {
        const tmp = LocationPresenter.prototype.getInfo;
        LocationPresenter.prototype.getInfo = jest.fn();
        
        new LocationPresenter(id);
        expect(LocationPresenter.prototype.getInfo).toHaveBeenCalledTimes(1);
    
        LocationPresenter.prototype.getInfo = tmp;
    })

    if(id != 6) {
        describe('2 - get info - should find', () => {
            test('google api ready', async () => {
                google_ready.set(true);
                const presenter = new LocationPresenter(id);
        
                jest.runAllTimers();
                expect(get(presenter.info)).resolves.toBeTruthy();
                const info = await get(presenter.info);
                expect(info).toBeTruthy();
                expect(info.address).toBeTruthy();
                expect(info.img).toBeTruthy();
                if(!info.img.alt) {
                    expect(info.img.height).toBeTruthy();
                    expect(info.img.width).toBeTruthy();
                    expect(info.img.url).toBeDefined();
                    expect(info.img.alt).toBeDefined();
                }
                expect(info.name).toBeTruthy();
                expect(info.score).not.toStrictEqual(undefined);
                expect(info.phone_number).toBeDefined();
                expect(info.website).toBeDefined();
                expect(info.types).toBeTruthy();
                expect(info.types).not.toContain("establishment");
                expect(info.types).not.toContain("point of interest");
        
                expect(info.name.charAt(0) == info.name.charAt(0).toUpperCase()).toBeTruthy();
                expect(info.address.charAt(0) == info.address.charAt(0).toUpperCase()).toBeTruthy();
            })
        
            test('google api not ready', () => {
                google_ready.set(false);
                const presenter = new LocationPresenter(id);
                expect(presenter.info).toBeTruthy();
                jest.runAllTimers();
                expect(get(presenter.info)).rejects.toEqual(new RequestError(404, "Timeout on loading google api"));
            })
        });
    } else {
        describe('2 - get info - should not find', () => {
            test('google api ready', async () => {
                google_ready.set(true);
                const presenter = new LocationPresenter(id);
                jest.runAllTimers();
                expect(get(presenter.info)).rejects.toEqual(new RequestError(404, "Error with request to G_API"));
            })
        
            test('google api not ready', () => {
                google_ready.set(false);
                const presenter = new LocationPresenter(id);
                expect(presenter.info).toBeTruthy();
                jest.runAllTimers();
                expect(get(presenter.info)).rejects.toEqual(new RequestError(404, "Timeout on loading google api"));
            })
        });
    }
})
