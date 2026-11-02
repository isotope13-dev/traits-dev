// Benign heartbeat: posts only the app version and hostname.
// No host inventory, no IP discovery, no remote stage handling.
const axios = require('axios');
const os = require('os');

async function heartbeat(url, version) {
  await axios.post(url, {
    version,
    host: os.hostname(),
    ts: Date.now()
  });
}

heartbeat('https://ingest-07.example-ops.net/heartbeat', '1.2.3');
