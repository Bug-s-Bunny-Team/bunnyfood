<script lang="ts">
    import { ChangePswPresenter } from '../presenters/ChangePswPresenter';
    let new_password;
    let repeat_password;
    let loading;
    let presenter = new ChangePswPresenter();

    const handleSubmit=()=>{
        const changepswFields={
            "NewPsw": new_password,
            "RepeatPsw": repeat_password,
     }
     console.log(changepswFields)
   }

</script>

    <h2>Change your password</h2>
    <form>
        <div class="inputBox">
            <label for="userPassword">Current Password</label>
            <input type="password" name="userPassword" id="userPassword" placeholder="type your current password" required on:click={presenter.handleChangePsw}/> 
        </div>
        <div class="inputBox">
            <label for="newuserPassword">New Password</label>
            <input type="password" name="userPassword" id="newuserPassword" placeholder="type your new password" required on:click={presenter.handleChangePsw}/> 
        </div>
        <div class="inputBox">
            <label for="reapuserPassword">Confirm Password</label>
            <input type="password" name="userPassword" id="reapuserPassword" placeholder="type your new password again" required on:click={presenter.handleChangePsw}/> 
        </div>
            <button type="submit" name="" style="float: left;">Submit</button>
    </form>
<footer>
</footer>
