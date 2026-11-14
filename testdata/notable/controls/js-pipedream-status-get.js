const https = require('https');

https.get('https://eosrhixgl4px9ae.m.pipedream.net/', (response) => {
  response.resume();
});
