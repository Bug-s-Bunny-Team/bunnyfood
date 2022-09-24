import App from './App.svelte'
import { mock_fetch } from '../tests/integration/mock_server'

const app = new App({
  target: document.getElementById('app')
})

if(import.meta.env.DEV) {
  window.fetch = mock_fetch;
}

export default app
