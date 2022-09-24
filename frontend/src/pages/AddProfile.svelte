<script>
    import { onDestroy } from 'svelte/internal';
    import { AddProfilesPresenter } from "../presenters/AddProfilesPresenter";
    let presenter = new AddProfilesPresenter();
    let {searchText, disableButtons, profile} = presenter;
    onDestroy(presenter.destroy);
</script>

<article> 
    <form on:submit|preventDefault={presenter.search} autocomplete="off">
    <div class="grid">
    <label for="scrape-input">
        Search for a profile
                <input
                    type="search"
                    id="scrape-input"
                    bind:value={$searchText}
                    placeholder="testuser123"
                    required
                    disabled={$disableButtons}
                    pattern="^[^\s]+$"
                />
    </label>
    <button id="submit" type="submit" disabled={$disableButtons}> Search </button>
    </div>
    </form>
</article>

{#if $profile} 
    {#await $profile}
        Searching profile...
        <progress />
    {:then _profile} 
        {#if _profile}
            <div class="grid">
                <article>
                    <header>
                        <strong>Username</strong>: {_profile.username}
                    </header>
                    <strong>Followers</strong>: {_profile.followers_count}
                    <footer>
                        <button disabled={$disableButtons} on:click={() => {presenter.addProfile(_profile)}}><strong>Segui</strong></button>
                    </footer>            
                </article>
            </div>
        {:else if _profile === undefined}
            <p>You already follow this account</p>
        {:else}
            <p>Couldn't find profile. <strong>You must enter the correct and full username of the profile</strong></p>
        {/if}
    {:catch}
        <p>There has been an error, please try again</p>
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
