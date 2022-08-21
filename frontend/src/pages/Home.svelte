<script lang="ts">
    import Map from "./Map.svelte";
    import ListView from "./ListView.svelte";
    import { HomePresenter } from "../presenters/HomePresenter";
    import Location from "./Location.svelte";
    export let currentRoute: any;
    currentRoute.queryParams = {};

    let presenter = new HomePresenter();
</script>

<label for="choose view"> 
    View as Map
    <input type="checkbox" id="choose" role="switch" bind:checked={presenter.mapView}> 
</label>

{#if presenter.mapView}
    <Map/>
{:else}
    <ListView/>
{/if}

{#if currentRoute.queryParams.details_placeid}
    <article class="popup">
        <header><a href="/home">Close</a></header>
        <Location placeid={parseInt(currentRoute.queryParams.details_placeid)}/>
    </article>
{/if}


<style>
    .popup {
        position: absolute;
        top: 2em;
        left: 10%;
        width: 80%;
        max-height: 80%;
        overflow-y: auto;
        z-index: 50;
        padding-top: 0;
    }
    .popup header {
        position: sticky;
        top: 0;
        z-index: 51;
    }
</style>









