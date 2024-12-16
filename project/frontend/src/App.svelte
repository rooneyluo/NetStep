<!-- src/App.svelte -->
<script>
    import { Router, Link, Route } from 'svelte-routing';
    import { onMount } from 'svelte';
    import Home from './routes/Home.svelte';
    import Login from './routes/Login.svelte';
    import Register from './routes/Register.svelte';
    import { isLoggedIn } from './stores.js';  
    import { logout, verify_token } from './lib/auth.js';  
    import { db_test } from './lib/db.js';
    import Event from './routes/Event.svelte';

    let loggedIn;
    isLoggedIn.subscribe(value => loggedIn = value);

    // On page load, check if user is already logged in (validate JWT)
    onMount(async () => {
        verify_token();  // Check if JWT is valid
    });
    
</script>

<main>
    <Router>
        <nav>
            <Link to="/">Home</Link>
            {#if loggedIn}
                <button on:click={db_test}>DB-Test</button>
                <button on:click={logout}>Logout</button> <!-- Show Logout when logged in -->
                <Link to="/create_event">Create Event</Link> <!-- Show Create Event when logged in -->
            {:else}
                <Link to="/login">Login</Link>
                <Link to="/register">Register</Link>
            {/if}
        </nav>

        <Route path="/" component={Home} />
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />
        <Route path="/create_event" component={Event} />
    </Router>
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>
