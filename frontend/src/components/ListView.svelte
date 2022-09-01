<script lang="ts">
    import { ListPresenter } from "../presenters/ListPresenter";
    import { capitalizeFirstLetter } from "../utils";

    let presenter = new ListPresenter();
    let {rankedList, disableButtons} = presenter;

    import StarRating from 'svelte-star-rating';

    const config = {
        emptyColor: 'hsl(240, 80%, 85%)',
        fullColor: '#FFFF00',
        showText: false,
        size: 42,
    };
    const style = 'display: inline; padding: 0.2em 1em; padding-bottom: 0.6em;';

</script>

<div>
    <button class="refresh outline" disabled={$disableButtons} on:click={presenter.refresh}>Refresh</button>
    
    {#await $rankedList}
        <p>Loading locations...</p>
        <progress />
    {:then locations} 
        {#if locations.length > 0}
            <div class="grid">
                {#each locations as location}
                    <article>
                        <header>
                            <strong>Location</strong>: <a href="./home?details_placeid={location.id}">{capitalizeFirstLetter(location.name)}</a>
                        </header>
                        {#if location.score !== null}
                            <p><strong>Score</strong>: <StarRating rating={Math.round(location.score*10.0)/10.0} {config} {style}/></p>
                        {:else}
                            <p>The Score is unavailable</p>
                        {/if}
                </article>
                {/each}
            </div>
        {:else}
            <p>No locations</p>
        {/if}
    {:catch}
        <p>There has been an error, please try again</p>
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
        margin-top: 0.5em;
        margin-left: 0.5em;
        padding: 0.5em;
    }
    .grid {
        grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
    }
</style>
