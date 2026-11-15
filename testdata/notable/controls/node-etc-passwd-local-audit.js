const fs = require('fs');
fs.readFile('/etc/passwd', 'utf8', (error, content) => {
  if (!error) console.log(content.split('\n').length - 1);
});
