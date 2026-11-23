const fs = require('fs');
const cp = require('child_process');
const manualRestart = 'tell application "System Events" to restart';
const plist = `<dict><key>ProgramArguments</key><array><string>/bin/echo</string><string>hello</string></array>
<key>RunAtLoad</key><true/><key>StartInterval</key><integer>420</integer></dict>`;
fs.writeFileSync('/Library/LaunchAgents/com.example.status.plist', plist);
cp.execFileSync('launchctl', ['load', '/Library/LaunchAgents/com.example.status.plist']);
