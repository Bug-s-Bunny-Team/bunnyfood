import { jest } from '@jest/globals'
import { AccountModel } from './src/models/accountModel';

jest.mock('./src/models/accountModel');

AccountModel.getInstance().createAccount();
