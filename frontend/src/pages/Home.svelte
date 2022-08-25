<script lang="ts">
    import Map from "../components/Map.svelte";
    import ListView from "../components/ListView.svelte";
    import { HomePresenter } from "../presenters/HomePresenter";
    import Location from "../components/Location.svelte";
    export let currentRoute: any;
    currentRoute.queryParams = {};
    let presenter = new HomePresenter();

    function okayPopUp(param: boolean):void {
        if (param == true) 
           document.getElementById("overlay").style.display = "block";
        else 
            document.getElementById("overlay").style.display = "none";
    }
</script>
<div id="overlay" > </div>
<div id="error"></div>

<label for="choose view"> 
    View as Map
    <input type="checkbox" id="choose" role="switch" bind:checked={presenter.mapView}> 
</label>

{#if presenter.mapView}
    <Map/>
{:else}
    <ListView/>
{/if}

{#if currentRoute.queryParams.details_placeid } 
    <article class="popup">
        {okayPopUp(true)}
        <header> <a href="/home" on:click={() => {okayPopUp(false)} }> Close </a> </header>
        <Location placeid={parseInt(currentRoute.queryParams.details_placeid)}/>
    </article>
{/if} 



<style>
    #overlay {
  position: fixed;
  display: none;
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
        top: 2em;
        left: 10%;
        width: 80%;
        max-height: 80%;
        overflow-y: auto;
        z-index: 50;
        padding: 0.2em;
        
    }
    .popup header {
        position: sticky;
        top: 0;
        z-index: 51;
    }

</style>









