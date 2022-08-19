<script lang="ts">

    import { RegistrationPresenter } from '../presenters/RegistrationPresenter';
    import { Navigate } from 'svelte-router-spa'
	
    let email;
    let password;
    let firstName;
    let lastName;
    let username;
    let loading;
    let presenter = new RegistrationPresenter();

    const handleSubmit=()=>{
        const signupFields={
            "FirstName": firstName,
            "LastName": lastName,
            "userName": username,
            "Email": [
                {
                "Type": "Primary",
                "Value": email
                }
            ],
            "Password": password
     }
     console.log(signupFields)
   }

   let errors = { firstName: '', lastName: '', userName: '',email: '', psw: ''};
    let valid = false;

    const addAccountHandler = () => {  
        if (valid) {
            console.log('valid', presenter.username)
        }
    }

    const handleInput = (event) => {
        valid = false

        if (presenter.firstname.trim().length <= 0) {
            valid = false;
            errors.firstName = 'Campo obbligatorio';
        }else {
            valid = true
            errors.firstName = '';
        }

        if (presenter.lastname.trim().length <= 0) {
            valid = false;
            errors.lastName = 'Campo obbligatorio';
        }else {
            valid = true
            errors.lastName = '';
        }

        if (presenter.email.trim().length <= 0) {
            valid = false;
            errors.email = 'Campo obbligatorio';
        }else {
            valid = true
            errors.email = '';
        }

        if (presenter.username.trim().length <= 0) {
            valid = false;
            errors.userName = 'Username deve essere inserito';
        }else {
            valid = true
            errors.userName = '';
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
 
 <h2>Register</h2>
    <form on:submit|preventDefault={addAccountHandler}>
        <div class="inputBox">
            <label for="firstName">First name</label>
            <input type="text" name="firstName" id="firstName" placeholder="type your first name" required bind:value={presenter.firstname} on:click={presenter.handleRegister} on:input={handleInput}/>
            <div class="error">{ errors.firstName }</div>
        </div>
        <div class="inputBox">
            <label for="lastName">Last name</label>
            <input type="text" name="lastName" id="lastName" placeholder="type your last name" required bind:value={presenter.lastname} on:click={presenter.handleRegister} on:input={handleInput}/>
            <div class="error">{ errors.lastName }</div>
        </div>
        <div class="inputBox">
            <label for="userName">Username</label>
            <input type="text" name="userName" id="userName" placeholder="type your username" required bind:value={presenter.username} on:click={presenter.handleRegister} on:input={handleInput}/>
            <div class="error">{ errors.userName }</div>
        </div>
        <div class="inputBox">
            <label for="userEmail">Email</label>
            <input type="email" name="userEmail" id="userEmail" placeholder="type your email"
            required bind:value={presenter.email} on:click={presenter.handleRegister} on:input={handleInput}/>
                   <div class="error">{ errors.email }</div>
        </div>
        <div class="inputBox">
            <label for="userPassword">Password</label>
            <input type="password" name="userPassword" id="userPassword" placeholder="type your password"
            required bind:value={presenter.password} on:click={presenter.handleRegister} on:input={handleInput}/>
                   <div class="error">{ errors.psw }</div>
        </div>
        <div class="inputBox">
            <label for="userConfirmPassword">Confirm Password</label>
            <input type="password" name="userPassword" id="userConfirmPassword" placeholder="confirm your password"
            required bind:value={presenter.confirmPsw} on:click={presenter.handleRegister} on:input={handleInput}/>
        </div>
        <button type="submit" name="" style="float: left;"  disabled={!valid} on:click={presenter.handleRegister}>Submit</button>
        <strong class="link"><Navigate to="/login">Login</Navigate></strong>
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
