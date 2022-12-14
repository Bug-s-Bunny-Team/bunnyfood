import { jest, test, describe, expect, beforeEach } from '@jest/globals';
import { get } from 'svelte/store';
import { Info, RequestError } from '../../../src/models';
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

    if(id != 1 && id != 6) {
        describe('2 - get info - should find', () => {
            test('google api ready', async () => {
                google_ready.set(true);
                const presenter = new LocationPresenter(id);
        
                jest.runAllTimers();
                await expect(get(presenter.info)).resolves.toBeTruthy();
                const info = await get(presenter.info);
                await Info.schema.validate(info);
        
                expect(info.name.charAt(0) == info.name.charAt(0).toUpperCase()).toBeTruthy();
                expect(info.address.charAt(0) == info.address.charAt(0).toUpperCase()).toBeTruthy();
            })
        
            test('google api not ready', async () => {
                google_ready.set(false);
                const presenter = new LocationPresenter(id);
                expect(get(presenter.info)).toBeTruthy();
                jest.runAllTimers();
                await expect(get(presenter.info)).rejects.toEqual(new RequestError(404, "Timeout on loading google api"));
            })

            test('google api not ready -> ready', async () => {
                google_ready.set(false);
                const presenter = new LocationPresenter(id);
                expect(get(presenter.info)).toBeTruthy();
                google_ready.set(true);
                jest.runAllTimers();
                await expect(get(presenter.info)).resolves.toBeTruthy();
                const info = await get(presenter.info);
                await Info.schema.validate(info);
        
                expect(info.name.charAt(0) == info.name.charAt(0).toUpperCase()).toBeTruthy();
                expect(info.address.charAt(0) == info.address.charAt(0).toUpperCase()).toBeTruthy();
            })
        });
    } else {
        describe('2 - get info - should not find', () => {
            test('google api ready', async () => {
                google_ready.set(true);
                const presenter = new LocationPresenter(id);
                expect(get(presenter.info)).toBeTruthy();
                jest.runAllTimers();
                await expect(get(presenter.info)).rejects.toEqual(new RequestError(404, "Error with request to G_API"));
            })
        
            test('google api not ready', async () => {
                google_ready.set(false);
                const presenter = new LocationPresenter(id);
                expect(get(presenter.info)).toBeTruthy();
                jest.runAllTimers();
                await expect(get(presenter.info)).rejects.toEqual(new RequestError(404, "Timeout on loading google api"));
            })

            test('google api not ready -> ready', async () => {
                google_ready.set(false);
                const presenter = new LocationPresenter(id);
                expect(get(presenter.info)).toBeTruthy();
                google_ready.set(true);
                jest.runAllTimers();
                await expect(get(presenter.info)).rejects.toEqual(new RequestError(404, "Error with request to G_API"));
            })
        });
    }
})
