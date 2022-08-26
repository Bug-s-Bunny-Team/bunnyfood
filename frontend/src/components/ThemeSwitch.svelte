<script>
    import { onMount } from "svelte";
    const STORAGE_KEY = "theme";
    const THEMES = {
        DARK: "dark",
        LIGHT: "light",
    };

    let currentTheme = THEMES.LIGHT;
    $: dark = currentTheme === THEMES.DARK;

    function toggleTheme() {
        currentTheme = currentTheme === THEMES.DARK ? THEMES.LIGHT : THEMES.DARK;
        localStorage.setItem(STORAGE_KEY, currentTheme);
        applyTheme();
    }

    function applyTheme() {
        document.getElementsByTagName("html")[0].dataset.theme = currentTheme;
    }

    onMount(() => {
        const stored = localStorage.getItem(STORAGE_KEY);

        if (stored) {
            currentTheme = stored;
        } else {
            localStorage.setItem(STORAGE_KEY, currentTheme);
        }

        applyTheme();
    });
</script>

<label for="dark-switch">
    <input
        type="checkbox"
        id="dark-switch"
        role="switch"
        on:change={toggleTheme}
        bind:checked={dark}
    />
</label>
