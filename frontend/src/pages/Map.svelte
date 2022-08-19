<script lang="ts">
    import type { Location } from '../models'
    import { MapPresenter } from '../presenters/MapPresenter.js';
    
    let presenter=new MapPresenter();
    let locations: Promise<Location[]>;
    presenter.rankedList.subscribe(_rankedList => {locations = _rankedList});
</script>

<svelte:window on:resize={presenter.resizeMap} />

{#await locations}
    <p>Loading locations...</p>
    <progress />
{:then _} 
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
        integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
        crossorigin=""/>
    
    <div style="height:80vh;width:100%" use:presenter.initMap/>
{/await}

<style>
    :root[data-theme="light"] {
        --spinner-invert: 0%
    }
    :root:not([data-theme="light"]) {
        --spinner-invert: 100%
    }
</style>
