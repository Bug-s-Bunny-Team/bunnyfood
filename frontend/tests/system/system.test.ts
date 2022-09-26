import '@testing-library/jest-dom';
import {render, fireEvent, screen} from '@testing-library/svelte';
import ThemeSwitch from '../../src/components/ThemeSwitch';
import Error from '../../src/components/Error';
import AddProfile from '../../src/pages/AddProfile';

describe('1 - ThemeSwitch', () => {
    test('Il tema cambia se premuto lo switch', async () => {

        const { container } = render(ThemeSwitch);
        const input = container.querySelector("input[type=checkbox]");

        //await fireEvent.change(input, { target: { value: "light" } });
        await fireEvent.click(input);

        expect(input).toBeChecked();
        expect(input).toHaveStyle({
            'background-color': 'white'
        })
        //expect(input.value).toBe("light");
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
        const input = screen.getByPlaceholderText('testuser123');
        fireEvent.change(input, {target: {value: 'tommasodifanta'}});
        expect(container.get).toBe("Couldn't find profile. You must enter the correct and full username of the profile");
    })
});

//Messaggi di errore dentro pagina;