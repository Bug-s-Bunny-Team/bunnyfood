import { get } from 'svelte/store';
import App from './App.svelte'
import { google_ready } from './store'

const app = new App({
  target: document.getElementById('app')
})

window.initialize = function() { // compiler error to ignore
  google_ready.set(true);
}

export default app
