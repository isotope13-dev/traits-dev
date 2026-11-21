// A client stores its own credentials and decodes its own media.
// None of these observations establishes remote code execution or exfiltration.
const https = require("node:https");
const {createDecipheriv} = require('node:crypto');
const labels = ['rotate', 'twofa'];
function decodeMedia(key, iv, ciphertext) {
  const decipher = createDecipheriv('aes-256-cbc', key, iv);
  return Buffer.concat([decipher.update(ciphertext), decipher.final()]);
}
async function signIn(store, credentials) {
  await store.saveCredentials(credentials);
}
