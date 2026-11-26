import { expect, it } from 'vitest';
import { readXml } from './reader.js';

it('entity expansion and external entities are not resolved', async () => {
  const xml = '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol"><!ENTITY lol2 "&lol;&lol;"><!ENTITY lol3 "&lol2;&lol2;"><!ENTITY xxe SYSTEM "file:///etc/passwd">]><testsuite name="s"><testcase classname="&xxe;" name="&lol3;"/></testsuite>';
  const data = await readXml(xml);
  expect(JSON.stringify(data)).not.toContain('root:');
});
