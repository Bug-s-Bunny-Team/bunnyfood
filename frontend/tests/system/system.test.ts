import '@testing-library/jest-dom';
import {render, fireEvent, screen} from '@testing-library/svelte';
import Home from '../../src/components/ThemeSwitch';
import Error from '../../src/components/Error';
import AddProfile from '../../src/pages/AddProfile';
import { AccountModel } from '../../src/models/accountModel'

jest.mock('../../src/models/accountModel')

beforeAll(async () => {
    await AccountModel.getInstance().createAccount();
})

describe('1 - ThemeSwitch', () => {
    test('Il tema cambia se premuto lo switch', async () => {

        const { container } = render(Home);
        const input = container.querySelector("input[type=checkbox]");

        await fireEvent.click(input);

        expect(input).toBeChecked();
        expect(input).toHaveStyle({
            'background-color': 'white'
        })
    })
});

describe('2 - Visualizzazione errore', () => {
    test('Viene visualizzato un messaggio di errore', async () => {

        render(Error, {message: 'Error Message'})
        const heading = screen.getByText('Error Message')
        expect(heading).toBeInTheDocument()
    })
});

describe('3 - Visualizzazione errore Not Found Profile', () => {
    test('Not Found Profile', async () => {
        const { container } = render(AddProfile);

        const input = screen.getByTestId("scrape-input");
        fireEvent.change(input, {target: {value: "thisusernamedoesnotexist38434"}});

        const btn = screen.getByTestId("search-btn");
        fireEvent.click(btn);

        const error = await screen.findByTestId("error");
        expect(error.textContent).toBe("Couldn't find profile. You must enter the correct and full username of the profile");
    })
});
