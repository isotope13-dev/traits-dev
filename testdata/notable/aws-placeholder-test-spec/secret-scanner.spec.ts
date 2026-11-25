import { describe, expect, it } from 'vitest';
import { containsSecretInText } from '../../src/lib/secret-scanner.js';

describe('containsSecretInText', () => {
  it.each([
    ['AWS access key ID', 'AWS_ACCESS_KEY_ID=AKIAABCDEFGHIJKL1234'],
  ])('detects %s', async (_name, content) => {
    expect(await containsSecretInText(content)).toBe(true);
  });
});
