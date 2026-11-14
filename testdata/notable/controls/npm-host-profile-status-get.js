const https = require('https');

https.get('https://status.example/package.json', (response) => {
  response.resume();
});
