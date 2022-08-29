import { jest, test, describe, expect, beforeAll, beforeEach } from '@jest/globals';
import { get } from 'svelte/store';
import { RequestError } from '../../../src/models';
import { LocationPresenter } from '../../../src/presenters/LocationPresenter'
import { google_ready } from '../../../src/store';

jest.mock('../../../src/models/locationModel');
jest.useFakeTimers();

beforeEach(() => {
    jest.clearAllMocks();
})

describe('LocationPresenter', () => {
    describe('google api ready', () => {
        beforeAll(() => {
            google_ready.set(true);
        })

        test('constructor', () => {
            const getInfo_spy = jest.spyOn(LocationPresenter.prototype, 'getInfo');
            new LocationPresenter(0);
            expect(getInfo_spy).toHaveBeenCalledTimes(1);
        })

        test('get info & adjust info', async () => {
            const presenter = new LocationPresenter(0);

            const info = await get(presenter.info);
            expect(info).toBeTruthy();
            expect(info.address).toBeTruthy();
            expect(info.img).toBeTruthy();
            expect(info.img.height).toBeTruthy();
            expect(info.img.width).toBeTruthy();
            expect(info.img.url).toBeTruthy();
            expect(info.name).toBeTruthy();
            expect(info.score).toBeTruthy();

            expect(info.name.charAt(0) == info.name.charAt(0).toUpperCase()).toBeTruthy();
            expect(info.address.charAt(0) == info.address.charAt(0).toUpperCase()).toBeTruthy();
        })
    });

    describe('google api not ready', () => {
        beforeAll(() => {
            google_ready.set(false);
        })

        test('constructor', () => {
            const getInfo_spy = jest.spyOn(LocationPresenter.prototype, 'getInfo');
            new LocationPresenter(0);
            jest.clearAllTimers();
            expect(getInfo_spy).toHaveBeenCalledTimes(1);
        })

        test('get info', () => {
            const presenter = new LocationPresenter(0);
            expect(presenter.info).toBeTruthy();
            expect(jest.runAllTimers).toThrow(new RequestError(404, "Timeout on loading google api"));
        })

    });


});

