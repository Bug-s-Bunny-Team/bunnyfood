<script lang="ts">
    import Followees from '../components/Followees.svelte';
    import { AccountPresenter } from '../presenters/AccountPresenter';
    let presenter = new AccountPresenter();
    let disableButtons: boolean;
    presenter.disableButtons.subscribe(_disableButtons => { disableButtons = _disableButtons });
</script>

<div id="error"></div>

<h2>My Account</h2>
<h3> Your personal information </h3>
<article>
    <form>
        <p> Name: { presenter.name }</p>
        <p> Email: { presenter.email }</p>

        <p>
            Choose your predefined guide:
            <label>
                <input type=radio id="choosePreferenceM" disabled={disableButtons} on:change={presenter.changePreference} bind:group={presenter.preference} value={1}>
                List
            </label>
            <label>
                <input type=radio id="choosePreferenceL" disabled={disableButtons} on:change={presenter.changePreference} bind:group={presenter.preference} value={0}>
                Map
            </label>
        </p>
        <p>
            <details>
                <summary>Show Followees</summary>
                <span><Followees/></span>
            </details>
        </p>
        <button on:click|preventDefault={presenter.logout} disabled={disableButtons} id="logout">Logout</button>
    </form>
</article>

<footer>
</footer>

<style>
    details > span {
        display: block;
        padding: 1em 2em;
    }
</style>
