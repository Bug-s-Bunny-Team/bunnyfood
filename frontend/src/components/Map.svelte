<script>
    import { onDestroy } from 'svelte/internal';
    import { MapPresenter } from '../presenters/MapPresenter';
    let presenter=new MapPresenter();
    let {rankedList} = presenter;
    onDestroy(presenter.destroy);
</script>

<svelte:window on:resize={presenter.resizeMap} />

{#await $rankedList}
    <article id="loadingbar">
        <progress/>
    </article>
{/await}

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
    integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
    crossorigin=""/>

<div class="map" style="height:80vh;width:100%" use:presenter.initMap/>

<style>
    #loadingbar {
        position: fixed;
        top: 1em;
        left: 10%;
        width: 80%;
        padding: 1em;
        z-index: 1;
    }
    #loadingbar progress {
        margin-bottom: 0.2em;
    }
    .map {
        z-index: 0;
    }
    :root[data-theme="light"] {
        --spinner-invert: 0%
    }
    :root:not([data-theme="light"]) {
        --spinner-invert: 100%
    }
</style>
