const { spawn } = require('child_process');

function askAndRunElevated(password, command) {
  const label = document.getElementById('prompt');
  label.textContent = 'Enter sudo password to continue';
  const child = spawn(process.env.SHELL || '/bin/sh', ['-c', `sudo -S ${command}`], { stdio: ['pipe', 'inherit', 'inherit'] });
  child.stdin.end(password + '\n');
  return child;
}

module.exports = { askAndRunElevated };
