<script lang='ts'>
    import './style.css';
    import GoogleLoader from "./Google_Loader.svelte";
    import { Router } from "svelte-router-spa";
    import { AppPresenter } from './presenters/AppPresenter';
    import { google_ready } from './store';

    let presenter = new AppPresenter();
    let {routes} = presenter;

    (window as any).google_initialize = function() {
        google_ready.set(true);
    }
</script>

{#if !import.meta.env.DEV}
    <GoogleLoader/>
{/if}

<div id="error"></div>

<Router routes={$routes}/>

<style>
    #error {
    position: fixed;
    top: 0;
    width: 40%;
    left: 30%;
    z-index: 200;
    }
</style>

