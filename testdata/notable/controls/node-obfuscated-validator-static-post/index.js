const crypto = require('crypto');
const algorithm = Buffer.from('c2hhMjU2', 'base64').toString();
const encoding = Buffer.from('aGV4', 'base64').toString();
const digest = crypto.createHash(algorithm).update('local fixture').digest(encoding);
fetch('https://telemetry.example.invalid/validation', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ digest }),
});
