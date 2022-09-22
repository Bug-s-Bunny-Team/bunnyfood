import { init, fetch } from '../../integration/integration'
import { expect, test, beforeAll } from '@jest/globals'
import { ProfilesModel } from '../../../src/models/profilesModel'
import { SocialProfile } from '../../../src/models';

window.fetch = fetch;

beforeAll(async () => {
    await init();
})

test('1 - getProfile', async () => {
    await expect(ProfilesModel.getInstance().getProfile('tulliovardanega')).resolves.toEqual(new SocialProfile(1, 'tulliovardanega', 1));
})