import { LocationModel } from "../../../src/models/locationModel";
import { expect, test, beforeAll, describe, jest } from '@jest/globals'
import { Filter, Info, RequestError } from '../../../src/models';
import { ResultsModel } from "../../../src/models/resultsModel";

jest.mock('../../../src/models/resultsModel')

const test_cases = [
    0, 1, 2, 3, 4, 5, 6
]

describe('TUF13', () => {
    test.each(test_cases)('1 - getInfo', async id => {
        await ResultsModel.getInstance().getRankedList(new Filter());
        const promise = LocationModel.getInstance().getInfo(id, document.createElement('div'));
        if(id != 1 && id != 6) {
            await expect(promise).resolves.not.toThrow();
            await Info.schema.validate(await promise);
        } else {
            await expect(promise).rejects.toEqual(new RequestError(404, "Error with request to G_API"));
        }
    });
});