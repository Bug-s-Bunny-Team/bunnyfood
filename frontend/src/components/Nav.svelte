<script lang="ts">

    import { NavPresenter } from "../presenters/NavPresenter";
    import ThemeSwitch from "./ThemeSwitch.svelte";
    const presenter = new NavPresenter();
    let routes;
    presenter.routes.subscribe(new_routes => {
        routes = new_routes;
    });

    export let currentRoute;

</script>

<nav class="container">
    <li class='left'><strong>BunnyFood</strong></li>
    <ul>
        {#each routes as route}
            <li>
                <a
                    class={currentRoute.name == route.name ? "current" : ""}
                    href={route.name}>{route.title}</a
                >
            </li>
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
</style>
