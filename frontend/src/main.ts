import { get } from 'svelte/store';
import App from './App.svelte'
import { google_ready } from './store'

const app = new App({
  target: document.getElementById('app')
})

export default app
