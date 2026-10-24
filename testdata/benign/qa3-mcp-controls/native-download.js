'use strict';
const fs = require('fs');
const path = require('path');
const https = require('https');
const os = require('os');
const home = os.homedir();

function nativeFilename() {
  const { platform, arch } = process;
  if (platform === 'linux' && arch === 'x64') return 'filelens.linux-x64-gnu.node';
  if (platform === 'linux' && arch === 'arm64') return 'filelens.linux-arm64-gnu.node';
  if (platform === 'darwin' && arch === 'x64') return 'filelens.darwin-x64.node';
  if (platform === 'darwin' && arch === 'arm64') return 'filelens.darwin-arm64.node';
  if (platform === 'win32' && arch === 'x64') return 'filelens.win32-x64-msvc.node';
  return null;
}

const file = nativeFilename();
if (!file) { console.warn('filelens: unsupported platform ' + process.platform + '-' + process.arch); process.exit(0); }
const dest = path.join(__dirname, '..', file);
if (!fs.existsSync(dest)) {
  const url = 'https://github.com/another-owner/filelens/releases/latest/download/' + file;
  console.log('filelens: downloading prebuilt binary for ' + process.platform + '-' + process.arch + '...');
  const f = fs.createWriteStream(dest);
  https.get(url, (res) => {
    if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
      https.get(res.headers.location, (r2) => { r2.pipe(f); r2.on('end', ()=>{ f.close(); console.log('filelens: binary installed.'); }); }).on('error', e=>{ try{fs.unlinkSync(dest);}catch{} console.warn('filelens: download failed: ' + e.message); process.exit(0); });
      return;
    }
    if (res.statusCode !== 200) { console.warn('filelens: no prebuilt binary on releases; run npm run build (cargo). status=' + res.statusCode); process.exit(0); }
    res.pipe(f);
    res.on('end', ()=>{ f.close(); console.log('filelens: binary installed.'); });
  }).on('error', (e) => { try { fs.unlinkSync(dest); } catch {} console.warn('filelens: download failed: ' + e.message); process.exit(0); });
}

