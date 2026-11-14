const https = require('https');

function pollStatus() {
  https.get('https://status.example.invalid/updates', (response) => {
    let body = '';
    response.on('data', (chunk) => { body += chunk; });
    response.on('end', () => {
      const messages = body.split('\n');
      console.log(messages[messages.length - 1]);
    });
  });
  setTimeout(pollStatus, 30000);
}

pollStatus();
