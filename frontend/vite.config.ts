import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [svelte()],
    define: {
        '__BUILD_TIMESTAMP__': JSON.stringify(new Date().toISOString())
    },
    server: {
        proxy: {
            '/api/profiles/popular': {
                target: 'http://127.0.0.1:5000/mock/popular_profiles.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/profiles\/popular/, '')
            },
            '/api/profiles': {
                target: 'http://127.0.0.1:5000/mock/social_profiles.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/profiles/, '')
            },
            '/api/locations': {
                target: 'http://127.0.0.1:5000/mock/locations.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/locations/, '')
            },
            /*'/api/followed/unfollow': {
                target: 'http://127.0.0.1:5000/mock/followed.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/dev-api\/followed\/unfollow/, '')
            },*/
            '/api/followed': {
                target: 'http://127.0.0.1:5000/mock/followed.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/followed/, '')
            },
            '/api/preferences': {
                target: 'http://127.0.0.1:5000/mock/preferences.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/preferences/, '')
            },
        }
    }
})
