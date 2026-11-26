'use strict';
const fs = require('node:fs');
const path = require('node:path');

function installTool(dir, bin = './bin/tool') {
  const target = path.join(path.resolve(dir), bin);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, '#!/bin/sh\necho ok\n');
  fs.chmodSync(target, 0o755);
  return target;
}

module.exports = { installTool };
