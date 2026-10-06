// Benign control: test harness starting a throwaway sshd against a temp
// directory. Writing a fixture authorized_keys there is test setup, not
// persistence: the keys are generated fresh and loopback-only.
import { mkdtempSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, it } from 'node:test';

describe('remote terminal over ssh', () => {
  it('starts its own sshd', () => {
    const dir = mkdtempSync(join(tmpdir(), 'sshd-test-'));
    writeFileSync(join(dir, 'authorized_keys'), readFileSync(join(dir, 'client_key.pub')), { mode: 0o600 });
  });
});
