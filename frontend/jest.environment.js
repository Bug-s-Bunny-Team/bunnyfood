import { jest } from '@jest/globals'

if(!document.getElementById("error")) {
    const error_div = document.createElement('div');
    error_div.id = "error";
    document.querySelector("body").appendChild(error_div);
}

