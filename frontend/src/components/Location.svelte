<script lang="ts">
    import type { Info } from "../models";
    import type { Writable } from "svelte/store";
    import { LocationPresenter } from "../presenters/LocationPresenter";
    export let placeid: number;
    let presenter: LocationPresenter;
    let info: Writable<Promise<Info>> = null;

    onMount(() => {
        presenter = new LocationPresenter(placeid);
        info = presenter.info;
    })

    import StarRating from 'svelte-star-rating';
    import { onMount } from "svelte";
    const config = {
        emptyColor: 'hsl(240, 80%, 85%)',
        fullColor: '#FFFF00',
        showText: false,
        size: 42,
    };
    const style = 'display: inline; padding: 0.2em 1em; padding-bottom: 0.6em;';
</script>

<div id="location">
    {#if $info}
        {#await $info}
            <progress/>
        {:then info} 
            <div class="content">
                <h1>{info.name}</h1>
                <img src={info.img.url} width={info.img.width} height={info.img.height} alt={info.img.alt}/>
                <article>
                    <p><em id="types">
                        {#each info.types as type}
                            <span>{type}</span>
                        {/each}
                    </em></p>
                    <p><strong>Adress</strong>: {info.address}</p>
                    <p><strong>Phone</strong>: <a href={'tel:'+info.phone_number}>{info.phone_number}</a></p>
                    {#if info.score !== null}
                        <p><strong>Score</strong>: <StarRating rating={Math.round(info.score*10.0)/10.0} {config} {style}/></p>
                    {:else}
                        <p>The Score is unavailable</p>
                    {/if}
                    {#if info.website}
                        <p><a href={info.website}>Website</a></p>
                    {/if}
                </article>
            </div>
        {:catch}
            <p>There has been an error, please try again</p>
        {/await}
    {/if}
</div>


<style>
    .content {
        display: grid;
        grid-template-rows: auto auto auto;
        grid-template-columns: 40% 60%;
        column-gap: 3em;
        row-gap: 1em;
        overflow: hidden;
    }

    h1 {
        text-align: center;
        margin: 0.6em 0em;
        grid-row: 1;
        grid-column: 1 / span 2;
    }
    article {
        display: flex;
        flex-direction: column;
        align-items: baseline;
        justify-content: space-evenly;
        grid-row: 2 / span 2;    
        grid-column: 1;    
    }
    img {
        grid-row: 2 / span 2;
        grid-column: 2;
        z-index: 0;
    }

    #types > span::after {
        content: ", ";
    }

    #types > span:last-child::after {
        content: "";
    }
</style>