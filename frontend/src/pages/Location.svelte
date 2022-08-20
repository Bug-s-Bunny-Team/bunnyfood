<script lang="ts">
    import type { Info } from "../models";
    import { LocationPresenter } from "../presenters/LocationPresenter";
    export let currentRoute: any;

    let presenter = new LocationPresenter(currentRoute.namedParams.name);
    let info: Promise<Info>;
    presenter.info.subscribe(_info => {info = _info});
</script>

{#await info}
    <progress/>
{:then info} 
    <h1>{info.name}</h1>
    <img src={info.img} alt=""/>
    <p>Address: {info.address}</p>
    <p>Tel: {info.cell}</p>
{/await}


<style>
    h1 {
        margin: 0.6em 0em;
    }
</style>