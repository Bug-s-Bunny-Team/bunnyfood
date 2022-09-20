<script>
    import { AccountModel } from "../models/accountModel";
    let completed;
    
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
            const redirect_url = encodeURIComponent(`${window.location.protocol}//${window.location.host}/`);
            window.location.href = `https://bunnyfood-dev.auth.eu-central-1.amazoncognito.com/login?client_id=2k5d4g58072evbdqloqkuksd5u&response_type=token&redirect_uri=${redirect_url}`;
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
{:catch}
    <p>There has been an error, please try again</p>
{/await}

<style>
</style>