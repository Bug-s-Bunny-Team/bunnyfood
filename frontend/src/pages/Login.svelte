<script>
    import { LoginPresenter } from '../presenters/LoginPresenter'    
    import { Navigate } from 'svelte-router-spa'
    let presenter = new LoginPresenter();

    /*let fields = { username: '', psw: '' };*/
    let errors = { username: '', psw: ''};
    let valid = false;

    const addAccountHandler = () => {  
        if (valid) {
            console.log('valid', presenter.username)
        }
    }

    const handleInput = (event) => {
        valid = false

        if (presenter.username.trim().length <= 0) {
            valid = false;
            errors.username = 'Username deve essere inserito';
        }else {
            valid = true
            errors.username = '';
        }

        if (presenter.password.trim().length <= 0) {
            valid = false;
            errors.psw = 'Password deve essere immessa';
        }else {
            valid = true
            errors.psw = '';
        }
        
    }
</script>

    <h2>Login</h2>
    <form on:submit|preventDefault={addAccountHandler}>
        <div class="inputBox">
            <label for="userName">Username</label>
            <input type="text" name="userName" id="userName" placeholder="type your username" required bind:value={presenter.username} on:input={handleInput}/>
            <div class="error">{ errors.username }</div>
        </div>
        <div class="inputBox">
            <label for="userPassword">Password</label>
            <input type="password" name="userPassword" id="userPassword" placeholder="type your password" required bind:value={presenter.password} on:input={handleInput}/>
            <div class="error">{ errors.psw }</div>
        </div>
        <div>
            <input type="checkbox" name="preference" id="remember" value="preference" on:change={presenter.RememberFields} bind:checked={presenter.remember} >
            <label for="preference" > remember </label> 
        </div>
        <div>
            <button name="" style="float: left;" disabled={!valid} on:click|preventDefault={presenter.handleLogin}>Submit</button>
            <strong class="link"><Navigate to="/register">Register</Navigate></strong>

        </div>
    </form>
<footer>
</footer>

<style>
    
    label{
        margin: 10px auto;
        text-align: left;
    }
    .error {
        font-weight: bold;
        font-size: 12px;
        color: red;
    }
</style>
