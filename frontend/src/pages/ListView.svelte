<script lang="ts">
    import type { Location } from "../models";
    import { ListPresenter } from "../presenters/ListPresenter";
    
    let presenter = new ListPresenter();
    let locations: Promise<Location[]>;
    let disableButtons: boolean;
    presenter.disableButtons.subscribe(_disableButtons => { disableButtons = _disableButtons; });
    presenter.rankedList.subscribe(_rankedList => {locations = _rankedList});
</script>

<div>
    <button class="refresh outline" disabled={disableButtons} on:click={presenter.refresh}>Refresh</button>
    
    {#await locations}
        <p>Loading locations...</p>
        <progress />
    {:then locations} 
        {#if locations.length > 0}
            <div class="grid">
                {#each locations as location}
                    <article>
                        <header>
                            <strong>Location</strong>: {location.name}
                        </header>
                        <strong>Score</strong>: {location.score}
                    </article>
                {/each}
            </div>
        {:else}
            <p>No locations</p>
        {/if}
    {/await}
</div>

<style>
    :root[data-theme="light"] {
        --spinner-invert: 0%
    }
    :root:not([data-theme="light"]) {
        --spinner-invert: 100%
    }
    article {
        margin-top: 1em;
        margin-bottom: 1em;
    }
    .refresh {
        display: inline;
        width: fit-content;
        margin-left: 0.5em;
        padding: 0.5em;
    }
    .grid {
        grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
    }
</style>
