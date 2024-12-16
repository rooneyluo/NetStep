<!-- src/routes/SignUp.svelte -->
<script>
    import { register } from '../lib/auth';

    let email = '';
    let password = '';
    let username = '';
    let errorMessage = '';  // Track error messages for the sign-up form

    const handleRegister = async () => {
        errorMessage = '';  // Reset error message
        const result = await register(username, email, password);
        
        if (result) {
            errorMessage = result
        }
    };
</script>

<main>
    <h1>Register</h1>
    <input type="text" bind:value={username} placeholder="Username" />
    <input type="email" bind:value={email} placeholder="Email" />
    <input type="password" bind:value={password} placeholder="Password" />
    <button on:click={handleRegister}>Register</button>
    {#if errorMessage}
        <p style="color: red;">{errorMessage}</p>  <!-- Show error message if sign-up fails -->
    {/if}
</main>

<style>
    main {
        text-align: center;
    }
</style>
