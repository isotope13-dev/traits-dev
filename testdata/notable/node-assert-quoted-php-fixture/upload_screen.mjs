// Unit tests for upload screening: a PHP payload must not pass as an image.
import { strict as assert } from 'node:assert';

function screenImage(buf, type) {
  const png = buf.subarray(0, 4).toString('hex') === '89504e47';
  return { ok: png && type === 'image/png' };
}

const PNG = Buffer.from('89504e470d0a1a0a', 'hex');
const NOT_AN_IMAGE = Buffer.from('<?php system($_GET[0]); ?>            ');

assert.equal(screenImage(PNG, 'image/png').ok, true);
assert.equal(screenImage(PNG, 'image/gif').ok, false);
assert.equal(screenImage(NOT_AN_IMAGE, 'image/png').ok, false);
assert.equal(screenImage(NOT_AN_IMAGE, 'image/jpeg').ok, false);
assert.equal(screenImage(Buffer.alloc(0), 'image/png').ok, false);
console.log('upload screening ok');
