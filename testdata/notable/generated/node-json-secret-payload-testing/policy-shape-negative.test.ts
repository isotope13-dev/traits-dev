import { validatePolicy } from '../doctor/policy';

describe('policy registration', () => {
  it('accepts a secret-bearing policy shape', () => {
    const payload = JSON.stringify({
      secrets: ['token-a', 'token-b'],
      files: ['a.txt'],
    });
    expect(validatePolicy(payload)).toBe(true);
  });
});
