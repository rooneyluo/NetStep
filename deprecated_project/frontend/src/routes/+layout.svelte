<script>
    export let title = 'NetStep';

    import { redirect } from '@sveltejs/kit';

    export async function load({ session }) {
        if (!session.user) {
            throw redirect(302, '/login');
        } else {
            throw redirect(302, '/dashboard');
        }
    }

</script>

<svelte:head>
    <title>{title}</title>
</svelte:head>

<slot />

