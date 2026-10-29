// Downloading an update description does not make a separate local command C2.
const https = require('https');
const { exec } = require('child_process');
https.get('https://updates.example/status', response => response.resume());
archive.on('end', () => complete()); exec(localCommand);
