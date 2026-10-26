import { buildRestartScript } from '../restart';

describe('windows restart quoting', () => {
  it('never shells out to findstr', () => {
    const script = buildRestartScript({ action: 'restart' });
    expect(script).not.toContain('findstr');
    expect(script).toContain('%~f0');
  });
});
