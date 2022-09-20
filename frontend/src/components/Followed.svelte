<script>
    import { onDestroy } from 'svelte/internal';
    import { FollowedPresenter } from '../presenters/FollowedPresenter';
    import { Navigate } from 'svelte-router-spa'

    let presenter = new FollowedPresenter();
    let {profiles, disableButtons} = presenter;

    onDestroy(presenter.destroy);
</script>

<div>    
    {#await $profiles}
        <p>Loading followed profiles...</p>
        <progress />
    {:then followed} 
        {#if followed.length > 0}
            <div class="grid">
                {#each followed as _followed}
                    <article>
                        <header>
                            <strong>Username</strong>: {_followed.username}
                        </header>
                        <strong>Followers</strong>: {_followed.followers_count}
                        <footer>
                            <button disabled={$disableButtons} on:click|preventDefault={() => {presenter.removeFollowed(_followed)}}><strong>Rimuovi</strong></button>
                        </footer>  
                    </article>
                {/each}
            </div>
        {:else}
            <p>You don't follow any accounts yet. <strong class="link"><Navigate to="/add">Search for profiles</Navigate></strong> or <strong class="link"><Navigate to="/explore">Explore most followed ones</Navigate></strong>.</p>
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
    .grid {
        grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
    }
</style>
