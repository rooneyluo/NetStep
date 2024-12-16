<script> 
    import { create_event } from '../lib/event.js';
    import { loggedInUser } from '../stores.js';  

    
    let user;
    loggedInUser.subscribe(value => user = value);

    let name = '';
    let location = '';
    let start_time = '';
    let end_time = '';
    let description = '';
    let errorMessage = '';  // Track error messages for the login form
  
    const handleCreateEvent = async () => {
      errorMessage = '';
      const result = await create_event(name, location, start_time, end_time, description, user.email);
  
      if (result) {
        errorMessage = result;
      }
    };
  </script>
  
  <main>
    <h1>Create Event</h1>
    <input type="name" bind:value={name} placeholder="Name" />
    <input type="location" bind:value={location} placeholder="Location" />
    <input type="datetime-local" bind:value={start_time} placeholder="Start Time" />
    <input type="datetime-local" bind:value={end_time} placeholder="End Time" />
    <input type="Description" bind:value={description} placeholder="Description" />
    <button on:click={handleCreateEvent}>Confirm</button> 
    
    {#if errorMessage}
      <p style="color: red;">{errorMessage}</p>
    {/if}
  </main>
  
  <style>
    main {
        text-align: center;
    }
  </style>
  