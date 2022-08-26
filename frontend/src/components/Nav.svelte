<script lang="ts">

    import { NavPresenter } from "../presenters/NavPresenter";
    import ThemeSwitch from "./ThemeSwitch.svelte";
    import wallpaperUrl from "../assets/sfondo.png";

    const presenter = new NavPresenter();
    let routes;
    presenter.routes.subscribe(new_routes => {
        routes = new_routes;
    });

    export let currentRoute;

</script>
<img class="pic" src="{wallpaperUrl}" alt="sfondo" />

<nav id="bar">
    <ul>
        {#each routes as route}
            {#if route.visible}
                <li>
                    <a
                        class={currentRoute.name == route.name ? "current" : ""}
                        href={route.name}>{route.title}</a
                    >
                </li>
            {/if}
        {/each}
        <li>
            <ThemeSwitch/>
        </li>
    </ul>
</nav>


<style>
    .current {
        --background-color: var(--primary-focus);
        --color: var(--primary-hover);
    }

    .pic {
    width: 1000px;
    height: 250px;
    display: block;
    text-align: center;
    margin: 1em auto;
    }

    nav {
        display: block;
    }

    #bar {
        position: sticky;
        background-color: #11191f;
        top:0;
        width: 100%;
        border: 2px solid rgb(1, 96, 17);
        border-left: none;
        border-right: none;
        text-align: center;
        margin: 0.5em 3em;
    }

        ul {
        display: block;
        list-style-type: disc;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        padding-inline-start: 40px;
    }

    #bar li {
        display: inline-block;
        padding: 0.5em 2em;
        font-size: 1em;
        font-weight: bold;
    } 
    

</style>
