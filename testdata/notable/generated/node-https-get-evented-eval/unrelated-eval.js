const https = require('https');
https.get('https://example.org/data', response => {
  response.on('data', chunk => console.log(chunk));
  response.on('end', () => console.log('complete'));
});
function runLocal(source) { return eval(source); }
