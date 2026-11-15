const fs = require('fs');
const path = '/home';
fs.readdir(path, (err, files) => {
  if (!err) console.log(JSON.stringify({ path, files }));
});
