const https = require('https');
const { spawn } = require('child_process');

https.get('https://updates.example.invalid/metadata.json', (response) => {
  response.resume();
  if (response.statusCode === 200) spawn('node', ['--version']);
});
