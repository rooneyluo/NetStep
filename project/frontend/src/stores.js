// src/stores.js
import { writable } from 'svelte/store';

export const isLoggedIn = writable(false);  // 默認為未登錄

export const loggedInUser = writable(null);  // 默認為 null