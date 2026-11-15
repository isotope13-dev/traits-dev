const http = require('http');

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const status = url.searchParams.get('status');
  res.end(status === 'ready' ? 'ok' : 'not ready');
}).listen(8080, '0.0.0.0');
