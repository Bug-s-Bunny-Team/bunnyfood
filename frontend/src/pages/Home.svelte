<script lang="ts">
    import Map from "./Map.svelte";
    import ListView from "./ListView.svelte";
    import { HomePresenter } from "../presenters/HomePresenter";
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

<style>

</style>









