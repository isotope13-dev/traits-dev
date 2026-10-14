// Scheme-selected client, either ternary spelling: testing `http:` picks
// the same client as testing `https:`. Both are one neutral capability.
const http = require('http');
const https = require('https');
function clientFor(url) {
  const u = new URL(url);
  return u.protocol === 'http:' ? http : https;
}
function labelFor(url) {
  const u = new URL(url);
  return u.protocol === 'https:' ? 'secure' : 'plain';
}
export { clientFor, labelFor };
