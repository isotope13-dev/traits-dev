#!/usr/bin/env node
// Self-daemonizing CLI miniature: copies its own binary beside itself
// (Windows file-lock workaround), chmods the copy, spawns it detached with
// unref, and polls its loopback /api/status endpoint until ready. The
// spawned "stage" is the program itself; nothing is downloaded.
import { chmodSync, copyFileSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { spawn } from "node:child_process";
import { join } from "node:path";

export function daemonBinaryPath(agentDir) {
  const source = process.execPath;
  const binDir = join(agentDir, "bin");
  mkdirSync(binDir, { recursive: true });
  const target = join(binDir, "daemon");
  if (existsSync(target)) return target;
  copyFileSync(source, target);
  chmodSync(target, 0o755);
  writeFileSync(join(binDir, ".daemon-stamp"), "ready");
  return target;
}

export async function waitForReady(host, port) {
  const response = await fetch(`http://${host}:${port}/api/status`);
  return response.ok;
}

export function spawnBackground(agentDir, host, port, script) {
  const child = process.env.PACKAGED
    ? spawn(daemonBinaryPath(agentDir), ["--serve", host, String(port)], {
        detached: true,
        stdio: "ignore",
        env: process.env,
      })
    : spawn(process.execPath, [script, "--serve", host, String(port)], {
        detached: true,
        stdio: "ignore",
        env: process.env,
      });
  child.unref();
}
