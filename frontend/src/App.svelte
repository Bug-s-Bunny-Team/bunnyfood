<svelte:head>
    <script async src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCVMx0kLnfUJbOXiiEBaQHL7CmtUDTkreI&libraries=places&callback=initialize" type="text/javascript"></script>
</svelte:head>

<script lang="ts">
    import './style.css';
    import { Router } from "svelte-router-spa";
    import { AppPresenter } from './presenters/AppPresenter';
    let presenter = new AppPresenter();
    let routes : any[];
    presenter.routes.subscribe(_routes => {routes=_routes});
</script>

<Router {routes}/>

