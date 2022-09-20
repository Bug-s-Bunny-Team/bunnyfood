<script>
    import { onDestroy } from 'svelte/internal';
    import Followed from '../components/Followed.svelte';
    import { AccountPresenter } from '../presenters/AccountPresenter';
    let presenter = new AccountPresenter();
    let {disableButtons, preference, name, email } = presenter;

    onDestroy(presenter.destroy);
</script>

<div id="error"></div>

<h1> Your personal information </h1>
<article>
    <form>
        <p> Name: { $name }</p>
        <p> Email: { $email }</p>

        <p>
            Choose your predefined guide:
            <label>
                <input type=radio id="choosePreferenceM" disabled={$disableButtons} on:change={presenter.changePreference} bind:group={$preference} value={1}>
                List
            </label>
            <label>
                <input type=radio id="choosePreferenceL" disabled={$disableButtons} on:change={presenter.changePreference} bind:group={$preference} value={0}>
                Map
            </label>
        </p>
        <p>
            <details>
                <summary>Show Followed</summary>
                <div><Followed/></div>
            </details>
        </p>
        <button on:click|preventDefault={presenter.logout} disabled={$disableButtons} id="logout">Logout</button>
    </form>
</article>

<footer>
</footer>

<style>
    h1 {
        --font-size: 1.5rem;
    }
    details > div {
        padding: 1em 2em;
    }
</style>
