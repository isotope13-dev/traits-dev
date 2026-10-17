// Presence telemetry: only whether credentials are set is reported, never
// a secret value. Must stay clean.
const present = Boolean(process.env.API_TOKEN || process.env.SECRET);
await fetch('https://telemetry.example.com/ping', {
  method: 'POST',
  body: JSON.stringify({present, ts: Date.now()}),
});
