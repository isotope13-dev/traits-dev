'use strict';
// Enterprise control: pins the OFFICIAL provider endpoint through the
// same managed stores. No lookalike origin, so the hijack composites
// must stay silent here.
const cp = require('child_process');

const GATEWAY_URL = 'https://api.anthropic.com';
const REG_KEY = 'HKCU\\SOFTWARE\\Policies\\Claude';
const MAC_DOMAIN = 'com.anthropic.claudefordesktop';

function applyPolicy(url, apiKey) {
  cp.execFileSync('reg.exe', ['add', REG_KEY, '/v', 'inferenceGatewayBaseUrl', '/t', 'REG_SZ', '/d', url, '/f']);
  cp.execFileSync('reg.exe', ['add', REG_KEY, '/v', 'inferenceGatewayApiKey', '/t', 'REG_SZ', '/d', apiKey, '/f']);
  cp.execFileSync('defaults', ['write', MAC_DOMAIN, 'inferenceGatewayBaseUrl', '-string', url]);
  const config = {
    inferenceGatewayBaseUrl: url,
    inferenceGatewayApiKey: apiKey,
  };
  return config;
}

module.exports = { applyPolicy };
