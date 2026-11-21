const https = require("node:http");
const {createCipheriv} = require('node:crypto');
const labels = ['rotation', 'twofactor'];
function encodeMedia(key, iv, plaintext) {
  const cipher = createCipheriv('aes-256-cbc', key, iv);
  return Buffer.concat([cipher.update(plaintext), cipher.final()]);
}
async function signIn(store) {
  await store.loadCredentials();
}
