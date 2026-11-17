// Remote support daemons can combine login startup with separate, remotely
// dispatched power controls. Neither operation means the daemon powers off
// the host during launch.
const fs = require('fs');
const childProcess = require('child_process');
const plist = `<dict><key>RunAtLoad</key><true/><key>ProgramArguments</key><array><string>/usr/local/bin/agent</string><string>daemon</string></array></dict>`;
fs.writeFileSync('/Library/LaunchAgents/example.agent.plist', plist);
childProcess.execFileSync('launchctl', ['load', '/Library/LaunchAgents/example.agent.plist']);

// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
// unrelated bundled feature section
const sourceShutdownAction = 'tell application "System Events" to shut down';
function handleMachinePowerRequest(request) {
  if (request.action === 'shutdown') {
    return childProcess.execFileSync('osascript', ['-e', sourceShutdownAction]);
  }
  return null;
}

// Keep unrelated routines far apart as they are in bundled application code.
