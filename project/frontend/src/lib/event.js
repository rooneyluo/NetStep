import { navigate } from 'svelte-routing';

export const create_event = async (name, location, start_time, end_time, description, create_by) => {
    try {
        const response = await fetch('http://localhost:8000/create_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, location, start_time, end_time, description, create_by }),
            credentials: 'include',  // Important to include cookies
        });

        if (response.ok) {
            navigate('/'); 
            return null;
        }
    }
    catch (error) {
        console.error(error);
    }
}

export const get_events = async () => {
    try {
        const response = await fetch('http://localhost:8000/get_events', {
            method: 'GET',
            credentials: 'include',  // Important to include cookies
        });

        if (response.ok) {
            const events = await response.json();
            return events;
        }
    }
    catch (error) {
        console.error(error);
    }
}