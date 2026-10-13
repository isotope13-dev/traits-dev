// Agent-runner app dir module path: the runner keeps its venv and cached
// sources under ~/.melaya-runner/, so PYTHONPATH=~/.melaya-runner/ already
// makes `import helpers` resolve to the cached source at spawn time. A
// well-known agent-runner dotdir is conventional layout, not a hijack.
import { spawn } from "child_process";
import { join } from "path";
import { homedir } from "os";

const CACHE_DIR = join(homedir(), ".melaya-runner");

export function spawnHelper(script) {
  return spawn("python3", [script], {
    stdio: "inherit",
    env: { ...process.env, PYTHONPATH: CACHE_DIR },
  });
}
