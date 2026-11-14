const https = require('https');
const botToken = '123456789:AAABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi';

function sendTelegramMessage(text) {
  return https.request({
    hostname: 'api.telegram.org',
    path: `/bot${botToken}/sendMessage`,
    method: 'POST',
  });
}

sendTelegramMessage('Build completed successfully');
