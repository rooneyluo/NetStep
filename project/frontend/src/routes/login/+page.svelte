<script>
    let email = '';
    function handleLogin() {
        console.log(`Logging in with email: ${email}`);
        // 在此處添加後端 API 調用邏輯
    }

    function handleSocialLogin(provider) {
        console.log(`Logging in with ${provider}`);
        // 在此處添加社交登入邏輯
    }
</script>

<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        font-family: Arial, sans-serif;
    }
    h1 {
        margin-bottom: 20px;
    }
    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        width: 300px;
    }
    input {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 14px;
    }
    button {
        width: 100%;
        padding: 10px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        cursor: pointer;
    }
    .primary {
        background-color: #374151;
        color: white;
    }
    .secondary {
        background-color: #d1d5db;
        color: #111827;
    }
    .social {
        background-color: #d1d5db;
        color: #111827;
        margin-top: 10px;
    }
    a {
        color: #374151;
        text-decoration: none;
        font-size: 12px;
    }
    a:hover {
        text-decoration: underline;
    }
</style>

<main>
    <h1>Login</h1>
    <form on:submit|preventDefault={handleLogin}>
        <input
            type="email"
            placeholder="Email"
            bind:value={email}
            required
        />
        <a href="/signup">Create account</a>
        <button type="submit" class="primary">Next</button>
    </form>
    <button class="social" on:click={() => handleSocialLogin('LINE')}>
        Continue with LINE
    </button>
    <button class="social" on:click={() => handleSocialLogin('GOOGLE')}>
        Continue with GOOGLE
    </button>
</main>
