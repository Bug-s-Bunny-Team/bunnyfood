<script>
    import { onDestroy } from 'svelte/internal';
    import { ExplorePresenter } from "../presenters/ExplorePresenter";

    let presenter = new ExplorePresenter();
    let {profiles, disableButtons} = presenter;

    onDestroy(presenter.destroy);
</script>

<div>
    <button class="refresh outline" disabled={$disableButtons} on:click={presenter.refresh}>Refresh</button>
    
    {#await $profiles}
        <p>Loading most popular profiles...</p>
        <progress />
    {:then _profiles} 
        {#if _profiles.length > 0}
            <div class="grid">
                {#each _profiles as profile}
                    <article>
                        <header>
                            <strong>Username</strong>: {profile.username}
                        </header>
                        <strong>Followers</strong>: {profile.followers_count}
                        <footer>
                            <button disabled={$disableButtons} on:click={() => {presenter.addProfile(profile)}}><strong>Segui</strong></button>
                        </footer>  
                    </article>
                {/each}
            </div>
        {:else}
            <p>No profiles found</p>
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
