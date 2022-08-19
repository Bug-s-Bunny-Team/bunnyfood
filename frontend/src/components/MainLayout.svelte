<script lang="ts">
    import { Route } from "svelte-router-spa";
    import Nav from "./Nav.svelte";

    export let currentRoute;
    export let params = {};
</script>

<Nav {currentRoute} />
<main class="container">
    <Route {currentRoute} {params} />
</main>
