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
            // '/dev-api': {
            //     target: 'http://127.0.0.1:3000/',
            //     changeOrigin: true,
            //     rewrite: (path) => path.replace(/^\/dev-api/, '')
            // }
            '/dev-api/posts': {
                target: 'http://127.0.0.1:5000/mock/posts.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/dev-api\/posts/, '')
            },
            '/dev-api/profiles': {
                target: 'http://127.0.0.1:5000/mock/social_profiles.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/dev-api\/profiles/, '')
            },
            '/dev-api/results': {
                target: 'http://127.0.0.1:5000/mock/results.json',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/dev-api\/results/, '')
            }
        }
    }
})
