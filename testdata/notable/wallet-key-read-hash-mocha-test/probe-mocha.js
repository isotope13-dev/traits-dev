import { describe, it } from 'mocha';
import fs from 'node:fs';
import crypto from 'node:crypto';
describe('copy', () => {
  it('keeps the key intact', () => {
    const data = fs.readFileSync('test/data/pem/keys/a-private-node0.pem');
    crypto.createHash('sha384').update(data).digest('hex');
  });
});
