<script>
    import { login } from '../lib/auth.js';
  
    let email = '';
    let password = '';
    let errorMessage = '';  // Track error messages for the login form
  
    const handleLogin = async () => {
      errorMessage = '';
      const result = await login(email, password);
  
      if (result) {
        errorMessage = result;
      }
    };
  </script>
  
  <main>
    <h1>Please Log In</h1>
    <input type="email" bind:value={email} placeholder="Email" />
    <input type="password" bind:value={password} placeholder="Password" />
    <button on:click={handleLogin}>Login</button> 
    
    {#if errorMessage}
      <p style="color: red;">{errorMessage}</p>
    {/if}
  </main>
  
  <style>
    main {
        text-align: center;
    }
  </style>
  