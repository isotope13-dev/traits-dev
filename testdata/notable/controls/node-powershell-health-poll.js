const { execFile } = require('child_process');

const script = [
  '$count = 0',
  'while ($count -lt 3) {',
  '  Invoke-WebRequest -Uri "http://127.0.0.1:8080/health"',
  '  $count++',
  '  Start-Sleep 5',
  '}',
].join('\r\n');
execFile('powershell.exe', ['-NoProfile', '-Command', script]);
