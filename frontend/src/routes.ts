import MainLayout from "./components/MainLayout.svelte";
import ListView from "./pages/ListView.svelte";
import ChangePsw from "./pages/ChangePsw.svelte"
import Account from "./pages/Account.svelte";
import Explore from "./pages/Explore.svelte";
import Followees from "./pages/Followees.svelte";
import Map from "./pages/Map.svelte";
import AddProfile from "./pages/AddProfile.svelte";
import Login from "./pages/Login.svelte";
import Register from "./pages/Register.svelte";
import FirstPage from "./pages/FirstPage.svelte";
import Home from "./pages/Home.svelte";

const PublicRoutes = [
    {
        name: '/',
        title: 'FirstPage',
        component: FirstPage,
        layout: MainLayout,
        typeOfRoute: "public"
    },
    {
        name: '/login',
        title: 'Login',
        component: Login,
        layout: MainLayout,
        typeOfRoute: "public"
    },
    {
        name: '/register',
        title: 'Register',
        component: Register,
        layout: MainLayout,
        typeOfRoute: "public"
    }
]

const ProtectedRoutes = [
    {
        name: '/home',
        title: 'Home',
        component: Home,
        layout: MainLayout,
        typeOfRoute: 'private'
    },
    {
        name: '/changepsw',
        title: 'ChangePassword',
        component: ChangePsw,
        layout: MainLayout,
        typeOfRoute: 'private'
    },
    {
        name: '/account',
        title: 'Account',
        component: Account,
        layout: MainLayout,
        typeOfRoute: 'private'
    },
    {
        name: '/add',
        title: 'Add',
        component: AddProfile,
        layout: MainLayout,
        typeOfRoute: 'private'
    },
    {
        name: '/explore',
        title: 'Explore',
        component: Explore,
        layout: MainLayout,
        typeOfRoute: 'private'
    }
]

const routes = [...PublicRoutes, ...ProtectedRoutes]

export { routes, PublicRoutes, ProtectedRoutes }
