#!/usr/bin/env node
const https = require('https');
const args = process.argv.slice(2);
const content = args.join(' ').replace(/ /g, '-');
const encodedContent = encodeURIComponent(content);
const targetUrl = `https://api.example.invalid/search/${encodedContent}`;
const parsedUrl = new URL(targetUrl);
const options = {
  hostname: parsedUrl.hostname,
  path: parsedUrl.pathname,
  method: 'GET'
};
const req = https.request(options, () => {});
req.end();
