<script lang="ts">
    import './style.css';

    import { Router } from "svelte-router-spa";
    import { AppPresenter } from './presenters/AppPresenter';
    let presenter = new AppPresenter();
    let routes : any[];
    presenter.routes.subscribe(_routes => {routes=_routes});
</script>

<Router {routes} />

