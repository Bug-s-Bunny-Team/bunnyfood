import { test_fetch } from './tests/integration/integration'
import { test_google } from './tests/integration/integration';

if(!document.getElementById("error")) {
    const error_div = document.createElement('div');
    error_div.id = "error";
    document.querySelector("body").appendChild(error_div);
}

window.fetch = test_fetch;
window.google = test_google;