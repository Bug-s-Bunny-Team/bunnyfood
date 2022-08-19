<script lang="ts">
    import type { SocialProfile } from "src/models";
    import { AddProfilesPresenter } from "../presenters/AddProfilesPresenter";

    let presenter = new AddProfilesPresenter();
    let profiles: Promise<SocialProfile[]>;
    let disableButtons: boolean;
    presenter.disableButtons.subscribe(_disableButtons => { disableButtons = _disableButtons });
    presenter.profiles.subscribe(_profiles => { profiles = _profiles; });
</script>

<article> 
    <form on:submit|preventDefault={presenter.search} autocomplete="off">
    <div class="grid">
    <label for="scrape-input">
        Search a new profile
                <input
                    type="search"
                    id="scrape-input"
                    bind:value={presenter.searchText}
                    placeholder="testuser123"
                    required
                    disabled={disableButtons}
                    pattern="^[^\s]+$"
                />
    </label>
    <button id="submit" type="submit" disabled={disableButtons}> Search </button>
    </div>
    </form>
</article>

{#if profiles} 
    {#await profiles}
        Loading results...
        <progress />
    {:then profiles} 
        {#if profiles.length > 0}
            <div class="grid">
                {#each profiles as profile}
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
{/if}


<style>
    button {
        margin: auto;
    }

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
    .grid {
        grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
    }
</style>
