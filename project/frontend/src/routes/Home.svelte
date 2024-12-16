<!-- src/routes/Home.svelte -->
<script>
  import { onMount } from 'svelte';
  import { isLoggedIn, loggedInUser } from '../stores.js';  // 引入 Store
  import { get_events } from '../lib/event.js'

  let loggedIn;
  // 訂閱登入狀態變更
  isLoggedIn.subscribe(async value => {
    loggedIn = value;
    if (loggedIn) {
      events = await get_events();
    }
  });

  let userObj;
  loggedInUser.subscribe(value => userObj = value);  // 訂閱 Store
  let events = [];  // 儲存活動資訊

  onMount(async () => {
    if (loggedIn) {
      events = await get_events();  // 取得活動資訊
    }
  });
  

</script>

<main>
  {#if loggedIn}
      <!-- 已登入的內容，例如用戶儀表板或個人資料 -->
      <h1>Welcome back! {userObj.username}</h1>
      <h2>Upcoming Events</h2>
      <section class="events-container">
        {#if events.length > 0}
          {#each events as event}
            <div class="event-card">
              <h2>{event.name}</h2>
              <p><strong>Location:</strong> {event.location}</p>
              <p><strong>Start Time:</strong> {event.start_time}</p>
              <p><strong>End Time:</strong> {event.end_time}</p>
              <p><strong>Description:</strong> {event.description}</p>
            </div>
          {/each}
        {:else}
          <p>No events found.</p>
        {/if}
      </section>
  {:else}
      <!-- 未登入的內容 -->
      <h1>You are not logged in. You have to log in to access this page.</h1>
  {/if}

</main>

<style>
   main {
    text-align: center;
  }
  
  .events-container {
    max-height: 400px; 
    overflow-y: auto;
    padding: 1rem;
    border: 1px solid #ccc;
    margin-top: 1rem;
  }

  .event-card {
    background: #f9f9f9;
    border: 1px solid #ddd;
    padding: 1rem;
    margin-bottom: 1rem;
    text-align: left;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .event-card h2 {
    margin: 0 0 0.5rem 0;
  }

  .event-card p {
    margin: 0.25rem 0;
  }
</style>
