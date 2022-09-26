import App from './App.svelte'
import { mock_fetch, mock_google } from '../tests/integration/mock_server'
import { google_ready } from './store';

const app = new App({
  target: document.getElementById('app')
})

if(import.meta.env.DEV) {
  window.fetch = mock_fetch;
  window.google = mock_google;
  google_ready.set(true);
}
export default app
