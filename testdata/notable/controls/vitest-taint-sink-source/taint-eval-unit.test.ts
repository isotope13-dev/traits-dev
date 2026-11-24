import { describe, expect, it } from 'vitest';

const code = `function command(req) {
  eval(req.body);
}`;

describe('taint fixture source', () => {
  it('keeps the eval sink as fixture text', () => {
    expect(code).toContain('eval(req.body)');
  });
});
