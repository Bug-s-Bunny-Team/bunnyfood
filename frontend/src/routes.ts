import { AccountModel } from "./models/accountModel"; 
import MainLayout from "./components/MainLayout.svelte";
import Account from "./pages/Account.svelte";
import Explore from "./pages/Explore.svelte";
import AddProfile from "./pages/AddProfile.svelte";
import Home from "./pages/Home.svelte";
import NotFound from "./pages/NotFound.svelte";
import Root from "./pages/Root.svelte";

function isLogged() : boolean {
    return AccountModel.getInstance().getAccount() ? true : false;
}

export const routes = [
    {
        name: '/',
        title: '',
        onlyIf: { guard: () => {return !isLogged()}, redirect: '/home'},
        component: Root,
        layout: MainLayout,
        visible: false
    },
    {
        name: '/home',
        title: 'Home',
        onlyIf: { guard: isLogged, redirect: '/'},
        component: Home,
        layout: MainLayout,
        visible: true
    },
    {
        name: '/account',
        title: 'Account',
        onlyIf: { guard: isLogged, redirect: '/'},
        component: Account,
        layout: MainLayout,
        visible: true
    },
    {
        name: '/add',
        title: 'Add',
        onlyIf: { guard: isLogged, redirect: '/'},
        component: AddProfile,
        layout: MainLayout,
        visible: true
    },
    {
        name: '/explore',
        title: 'Explore',
        onlyIf: { guard: isLogged, redirect: '/'},
        component: Explore,
        layout: MainLayout,
        visible: true
    },
    {
        name: '404',
        onlyIf: { guard: isLogged, redirect: '/' },
        component: NotFound,
        layout: MainLayout,
        visible: false
    }
];
