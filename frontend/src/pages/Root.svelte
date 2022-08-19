<script lang="ts">
    import { AccountModel } from "../models/accountModel";

    if(AccountModel.getInstance().getAccount()) {
        window.location.pathname = '/home';
    } else {
        window.location.href = "https://aws.amazon.com/it/cognito/";
    }
</script>

<style>
</style>