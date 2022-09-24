<script>
    import Map from "../components/Map.svelte";
    import ListView from "../components/ListView.svelte";
    import { HomePresenter } from "../presenters/HomePresenter";
    import Location from "../components/Location.svelte";
    export let currentRoute;
    currentRoute.queryParams = {};
    let presenter = new HomePresenter();
    let { mapView } = presenter;
</script>

<label for="choose view"> 
    View as Map
    <input type="checkbox" id="choose" role="switch" bind:checked={$mapView}> 
</label>

{#if $mapView}
    <Map/>
{:else}
    <ListView/>
{/if}

{#if currentRoute.queryParams.details_placeid } 
    <div id="overlay"></div>
    <article style={'top: '+(document.documentElement.scrollTop || document.body.scrollTop)+'px;'} class="popup">
        <header><a href="/home"> Close </a></header>
        <Location placeid={parseInt(currentRoute.queryParams.details_placeid)}/>
    </article>
{/if} 



<style>
#overlay {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  z-index: 2;
  cursor: pointer;
}

.popup {
    position: absolute;
    margin-top: 2em;
    left: 10%;
    width: 80%;
    max-height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    z-index: 50;
    padding: 2em;
    padding-top: 0;
}
.popup header {
    position: sticky;
    top: 0;
    z-index: 51;
}

</style>









