const fs = require('fs');
const https = require('https');
const path = require('path');
const Seven = require('node-7z');

const archive = path.join(process.cwd(), 'bundle.zip');
https.get('https://updates.example.invalid/download/bundle.zip', (response) => {
  response.pipe(fs.createWriteStream(archive));
});

async function unpackUpdate(destination) {
  await Seven.extractFull(archive, destination, { password: 'bundle-key' });
}
