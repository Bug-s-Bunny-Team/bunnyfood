<script lang="ts">
    import { FolloweesPresenter } from '../presenters/FolloweesPresenter';
    import { Navigate } from 'svelte-router-spa'
    import type { SocialProfile } from 'src/models';

    let presenter = new FolloweesPresenter();
    let followees: Promise<SocialProfile[]>;
    presenter.profiles.subscribe(_profiles => {followees = _profiles});
</script>

<div>    
    {#await followees}
        <p>Loading followed profiles...</p>
        <progress />
    {:then followees} 
        {#if followees.length > 0}
            <div class="grid">
                {#each followees as followee}
                    <article>
                        <header>
                            <strong>Username</strong>: {followee.username}
                        </header>
                        <strong>Followers</strong>: {followee.followers}
                        <footer>
                            <button on:click|preventDefault={() => {presenter.removeFollowee(followee)}}><strong>Rimuovi</strong></button>
                        </footer>  
                    </article>
                {/each}
            </div>
        {:else}
            <p>You don't follow any accounts yet. <strong class="link"><Navigate to="/add">Search for profiles</Navigate></strong> or <strong class="link"><Navigate to="/explore">Explore most followed ones</Navigate></strong>.</p>
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
    .grid {
        grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
    }
</style>
