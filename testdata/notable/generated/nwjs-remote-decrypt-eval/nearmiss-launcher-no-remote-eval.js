// Near-miss: a desktop launcher opens a user-chosen path with a concatenated
// start argument and fetches a fixed feed. It never decrypts or evals data,
// so the remote-config composites must not fire.
const axios = require('axios');
const { execSync } = require('child_process');

function openDownloads(folder) {
  axios.get('https://feeds.example-desk.test/status.xml').then(() => {});
  execSync("start " + folder);
}

module.exports = { openDownloads };
