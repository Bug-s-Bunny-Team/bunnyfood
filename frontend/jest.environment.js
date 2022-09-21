import { jest } from '@jest/globals'
import { AccountModel } from './src/models/accountModel';

jest.mock('./src/models/accountModel');

if(!document.getElementById("error")) {
    const error_div = document.createElement('div');
    error_div.id = "error";
    document.querySelector("body").appendChild(error_div);
}

AccountModel.getInstance().createAccount();
