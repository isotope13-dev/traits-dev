const { exec } = require('child_process');
const os = require('os');
const hostname = os.hostname();
exec(`dig @1.1.1.1 health.example.com`, (_error, stdout) => {
  console.log(hostname, stdout);
});
