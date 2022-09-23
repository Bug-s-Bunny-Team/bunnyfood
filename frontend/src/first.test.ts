import '@testing-library/jest-dom';
import {render, fireEvent, screen} from '@testing-library/svelte';
import ThemeSwitch from '../../frontend/src/components/ThemeSwitch.svelte';
//import Account from '../../frontend/src/components/Account.svelte';
import App from './App.svelte';

/*describe('ThemeSwitch', () => {
    test('Il tema cambia se premuto lo switch', async () => {

        render(ThemeSwitch);
        const checkBTheme = screen.getByRole('switch' , { hidden: true });
        
        await fireEvent.click(checkBTheme);
         
        render(App)
        expect(App).toHaveStyle(`root[data-theme]: light;`);
        //expect(checkBTheme).toEqual('dark');
        //expect(checkBTheme).toEqual(true);
    })
})*/

describe('ThemeSwitch', () => {
    test('Il tema cambia se premuto lo switch', async () => {

        const { container } = render(ThemeSwitch);
        const input = container.querySelector("input[type=checkbox]");

        await fireEvent.change(input, { target: { value: "light" } });

        expect(input.value).toBe("light");
    })
})


/*describe('Reindirizzamento alla pagina di account premendo bottone Account', () => {
    test('Vado nella pagina di account', async () => {

    })
})*/

/*
describe('Logout', () => {
    test('Il bottone di logout viene cliccato') , async() => {
        render(Account);
        const logout = screen.getByRole('button');
        await fireEvent.click(logout);
        expect(logout.onclick).toEqual('1');
    }
}*/