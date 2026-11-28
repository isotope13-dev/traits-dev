// Self-updater for a CLI: ask npm for the latest version, install it beside
// the running copy, and report what was installed.
import { spawnSync } from "node:child_process";

export function latestVersion() {
  const view = spawnSync("npm", ["view", "example-cli@latest", "version"], { encoding: "utf8" });
  return view.status === 0 ? view.stdout.trim() : null;
}

export function installBeside(dir, version) {
  const got = spawnSync("npm", ["install", "--prefix", dir, "--ignore-scripts", `example-cli@${version}`], { encoding: "utf8" });
  return got.status === 0;
}
