<script lang="ts">
    import { AccountModel } from "../models/accountModel";
    let completed: Promise<boolean>;
    
    if(!AccountModel.getInstance().getAccount()) {
        completed = (async () => {
            await AccountModel.getInstance().createAccount();
            if(AccountModel.getInstance().getAccount()) {return(true)}
            else {return(false)}
        })();
    }
    else {completed = new Promise(resolve => {resolve(true)})}
    
    completed.then(logged => {
        if(logged) {
            window.location.href = `${window.location.protocol}//${window.location.host}/home`;
        } else {
            window.location.href = "https://bunnyfood-dev.auth.eu-central-1.amazoncognito.com/login?client_id=2k5d4g58072evbdqloqkuksd5u&response_type=token&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F";
        }
    });
</script>

{#await completed}
    <p>Checking login...</p>
    <progress/>
{:then logged} 
    {#if logged}
        <p>Logged! Redirecting...</p>
    {:else}
        <p>Not Logged, Redirecting...</p>
    {/if}
{:catch error}
    <p>{error}</p>
{/await}

<style>
</style>