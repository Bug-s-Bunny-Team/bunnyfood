<script lang="ts">
    import type { Info } from "../models";
    import { LocationPresenter } from "../presenters/LocationPresenter";
    export let currentRoute: any;

    let presenter = new LocationPresenter(parseInt(currentRoute.namedParams.id));
    let info: Promise<Info>;
    presenter.info.subscribe(_info => {info = _info});

    import StarRating from 'svelte-star-rating';

    const config = {
        emptyColor: 'hsl(240, 80%, 85%)',
        fullColor: '#FFFF00',
        showText: false,
        size: 42,
    };
    const style = 'display: inline; padding: 0.2em 1em; padding-bottom: 0.6em;';
</script>

{#await info}
    <progress/>
{:then info} 
    <h1>{info.name}</h1>
    <img src={info.img.url} width={info.img.width} height={info.img.height} alt=""/>
    <article>
        <p>Address: {info.address}</p>
        <p>Score: <StarRating rating={Math.round((info.score+1.0)*25)/10.0} {config} {style}/></p>
    </article>
{/await}


<style>
    h1 {
        margin: 0.6em 0em;
    }
    article {
        position: absolute;
        z-index: 1;
        max-width: 40%;
        top: 8em;
        left: 3.2em;
        box-shadow: 5px 8px rgba(0, 0, 0, 0.1);
    }
    img {
        z-index: 0;
    }
</style>