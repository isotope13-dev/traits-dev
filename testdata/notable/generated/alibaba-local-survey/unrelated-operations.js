const http = require('http');
const fs = require('fs');
const metadata = 'http://100.100.100.200/latest/meta-data/';
function diagnostic() { return metadata.slice(0, 10); }
fs.writeFileSync('local.log', 'ordinary output');
diagnostic();
