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

<strong class="link"><link name="Cognito Login" href="https://aws.amazon.com/it/cognito/"/></strong>
<button on:click={login}>Automatic Login</button>

<style>
</style>