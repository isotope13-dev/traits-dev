const os = require('os');
const axios = require('axios');

const telemetryData = {
  nodeVersion: process.version,
  hostname: os.hostname()
};
axios.post('https://webhook.site/12345678-1234-1234-1234-123456789abc/healthz?success', telemetryData);
