const https = require('https');
https.get('https://198.51.100.19/status', {}, res => {
  const unrelated = { rejectUnauthorized: false };
  res.resume();
});
