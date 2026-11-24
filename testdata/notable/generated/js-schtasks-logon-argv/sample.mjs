import { spawnSync } from 'node:child_process';

// Register a per-user task that starts the helper at logon.
export function registerLogonTask(action) {
  return spawnSync('schtasks', ['/create', '/f', '/tn', 'helper', '/sc', 'onlogon', '/tr', action, '/rl', 'LIMITED']);
}
