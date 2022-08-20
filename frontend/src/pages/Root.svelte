<script lang="ts">
    import { AccountModel } from "../models/accountModel";

    if(AccountModel.getInstance().getAccount()) {
        window.location.pathname = '/home';
    } /*else {
        window.location.href = "https://aws.amazon.com/it/cognito/";
    }*/

    function login() {
        AccountModel.getInstance().login("automatic login email", "automatic login psw", false);
        window.location.pathname = '/home';
    }
</script>

<a role="button" href="https://aws.amazon.com/it/cognito/">Cognito Login</a>
<button on:click={login}>Automatic Login</button>

<style>
    a {
        display: block;
        margin: 2em 0em;
    }
</style>