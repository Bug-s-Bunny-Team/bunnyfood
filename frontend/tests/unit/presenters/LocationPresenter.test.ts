import { jest, test, describe, expect } from '@jest/globals';
import { get } from 'svelte/store';
import { RequestError } from '../../../src/models';

jest.mock('../../../src/models/locationModel');
jest.useFakeTimers();

import { LocationPresenter } from '../../../src/presenters/LocationPresenter'
import { google_ready } from '../../../src/store';

describe('LocationPresenter.getInfo', () => {
    test('normal', async () => {
        const presenter = new LocationPresenter(0);
        google_ready.set(true);
        presenter.getInfo();
        expect(presenter.info).toBeTruthy();
        const info = await get(presenter.info);
        
        expect(info).toBeTruthy();
        expect(info.address).toBeTruthy();
        expect(info.img).toBeTruthy();
        expect(info.img.height).toBeTruthy();
        expect(info.img.width).toBeTruthy();
        expect(info.img.url).toBeTruthy();
        expect(info.name).toBeTruthy();
        expect(info.score).toBeTruthy();
    });

    test('timeout', async () => {
        const presenter = new LocationPresenter(0);
        google_ready.set(false);
        presenter.getInfo();
        expect(presenter.info).toBeTruthy();
        
        let error : RequestError | null = null;
        try {
            jest.runAllTimers();
        } catch (e) {
            error=e;
        }

        expect(error).toEqual(new RequestError(404, "Timeout on loading google api"));
    });
});

