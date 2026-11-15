const https = require('https');
const fs = require('fs');
const os = require('os');
const path = require('path');

const output = fs.createWriteStream(path.join(os.tmpdir(), 'release-notes.txt'));
https.get('https://updates.example.net/release-notes.txt', (response) => {
  response.pipe(output);
});
