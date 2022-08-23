<script lang="ts">
    import type { RequestError } from "../models";
    export let error: RequestError;
</script>

<article>
    <p>Error {error.code}: {error.message}</p>
</article>

<style>
</style>