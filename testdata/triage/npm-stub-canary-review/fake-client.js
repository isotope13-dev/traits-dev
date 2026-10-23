const https = { get(value) { return value; } };
const encoded = Buffer.from('diagnostic').toString('base64');
https.get(`https://example.invalid/log?data=${encoded}`, () => {});
