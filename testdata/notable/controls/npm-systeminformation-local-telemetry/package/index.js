const axios = require('axios');
const si = require('systeminformation');

async function report() {
  const os = await si.osInfo();
  const versions = await si.versions();
  const time = await si.time();
  await axios.post('https://telemetry.example.invalid', { os, versions, time });
}

report();
