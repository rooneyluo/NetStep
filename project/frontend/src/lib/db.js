export const db_test = async () => {
    try {
        const response = await fetch('http://localhost:8000/db-test', {
            method: 'GET',
            credentials: 'include'  // Important to send cookies
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
        } else {
            console.log('db test failed');
        }
    } catch (error) {
        console.error('Error during db test:', error);
    }
}