const fs = require('fs'); const key = fs.readFileSync('/home/demo/.ssh/authorized_keys', 'utf8'); console.log(key);
