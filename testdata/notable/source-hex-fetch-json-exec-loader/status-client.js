const https = require('https');
const { exec } = require('child_process');
// Status client: fetches version metadata and prints it. Never executes fetched data.
function fetchStatus() {
  const req = https.request({ hostname: 'status.example.org', path: '/v.json', method: 'GET' }, (res) => {
    let body = '';
    res.on('data', (c) => { body += c; });
    res.on('end', () => {
      const j = JSON.parse(body);
      console.log('version', j.version);
    });
  });
  req.end();
}
function hexToText(h) {
  let t = '';
  for (let n = 0; n < h.length; n += 2) t += String.fromCharCode(parseInt(h.slice(n, n + 2), 16));
  return t;
}
exec('git status');
module.exports = { fetchStatus, hexToText };
