const { exec } = require('child_process');

exec('nslookup example.net', () => {});
