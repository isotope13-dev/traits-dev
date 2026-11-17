const {hostname, platform} = require('os');
async function register(origin) {
  return fetch(`${origin}/identity/device`, {
    method: 'POST',
    body: JSON.stringify({label: hostname().slice(0,120), platform:platform()})
  });
}
