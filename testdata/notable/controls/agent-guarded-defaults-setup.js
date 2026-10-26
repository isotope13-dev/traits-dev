'use strict';
// Fixture: guarded-defaults setup helper. Guardrail keys travel through
// the same helper-call shape, but the values keep the agent restricted
// (read-only sandbox, approval on request) and no provider or gateway is
// configured. Must not convict any guardrail-disable or gateway-reroute
// composite.
const fs = require('fs');
const os = require('os');
const path = require('path');

function setRootKey(store, key, value) {
  store[key] = value;
}

function applyGuardedDefaults() {
  const settings = {};
  setRootKey(settings, 'sandbox_mode', 'read-only');
  setRootKey(settings, 'approval_policy', 'on-request');
  const confPath = path.join(os.homedir(), '.codex', 'config.toml');
  fs.writeFileSync(confPath, JSON.stringify(settings, null, 2));
  console.log('Applied guarded defaults in ~/.codex/config.toml');
}

applyGuardedDefaults();
