<script>
    import Followees from './Followees.svelte';
    import { AccountPresenter } from '../presenters/AccountPresenter';
    import { Navigate } from 'svelte-router-spa'
    let presenter = new AccountPresenter();
    let isLogged;
    presenter.isLogged.subscribe( logged => { isLogged = logged; });
</script>

{#if isLogged} 
    <h2>My Account</h2>
    <h3> Your personal information </h3>
    <article>
        <form>
            <p> Name: { presenter.name }</p>
            <p> Email: { presenter.email }</p>
            <p> Follower: {presenter.followers} </p>

            <p>
                Choose your predefined guide:
                <label>
                    <input type=radio id="choosePreferenceM" on:change={presenter.changePreference} bind:group={presenter.preference} value={1}>
                    List
                </label>
                <label>
                    <input type=radio id="choosePreferenceL" on:change={presenter.changePreference} bind:group={presenter.preference} value={0}>
                    Map
                </label>
            </p>

            <p><strong class="link"><Navigate to="/changepsw">Change your password </Navigate></strong></p>
            <p>
                <details>
                    <summary>Show Followees</summary>
                    <span><Followees/></span>
                </details>
            </p>
            <button name="" id="logout" on:click={presenter.handleLogout}>Logout</button>
        </form>
    </article>
{:else}
    <article>
        <p>Non sei loggato, effettua il <strong class="link"><Navigate to="/login">Login</Navigate></strong>.</p>
    </article>
{/if}

<footer>
</footer>

<style>
    details > span {
        display: block;
        padding: 1em 2em;
    }
</style>
