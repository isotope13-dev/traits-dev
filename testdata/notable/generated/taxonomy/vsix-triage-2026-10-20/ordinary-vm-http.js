const https = require('https');
const vm = require('vm');
https.get('https://config.example.net/data', response => {
  let buffer = '';
  response.on('data', chunk => buffer += chunk);
  response.on('end', () => {
    const config = JSON.parse(buffer);
    const sandbox = vm.createContext({config});
    vm.runInContext('config.answer + 1', sandbox);
  });
});
