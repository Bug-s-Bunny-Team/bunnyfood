<script lang="ts">
    import type { SocialProfile } from "../models";
    import { ExplorePresenter } from "../presenters/ExplorePresenter";

    let presenter = new ExplorePresenter();
    let profiles: Promise<SocialProfile[]>;
    let disableButtons: boolean;
    presenter.disableButtons.subscribe(_disableButtons => {disableButtons = _disableButtons});
    presenter.profiles.subscribe(_profiles => {profiles = _profiles});
</script>

<div>
    <h2 class="title">Explore</h2>
    <button class="refresh outline" disabled={disableButtons} on:click={presenter.refresh}>Refresh</button>
    
    {#await profiles}
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
                        <strong>Followers</strong>: {profile.followers}
                        <footer>
                            <button on:click={() => {presenter.addProfile(profile)}}><strong>Segui</strong></button>
                        </footer>  
                    </article>
                {/each}
            </div>
        {:else}
            <p>No profiles found</p>
        {/if}
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
    .title {
        display: inline;
    }
    .refresh {
        display: inline;
        width: fit-content;
        margin-left: 0.5em;
        padding: 0.5em;
    }
    .grid {
        grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
    }
</style>
