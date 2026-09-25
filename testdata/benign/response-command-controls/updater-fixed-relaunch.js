// Self-updater: checks a release endpoint, then relaunches the local binary
// when the server reports a newer ready version. The spawned path is fixed;
// the server never supplies command text.
const https = require('https');
const { spawnSync } = require('child_process');

function checkForUpdates(current) {
  return new Promise((resolve) => {
    const req = https.request('https://updates.example.com/api/v1/check', { method: 'POST' }, (res) => {
      let data = '';
      res.on('data', (c) => { data += c; });
      res.on('end', () => {
        try {
          const info = JSON.parse(data);
          if (info.version && info.version !== current && info.ready === true) {
            spawnSync(process.execPath, ['--updated'], { stdio: 'inherit' });
          }
        } catch (e) { /* ignore malformed responses */ }
        resolve();
      });
    });
    req.on('error', () => resolve());
    req.write(JSON.stringify({ version: current }));
    req.end();
  });
}

module.exports = { checkForUpdates };
