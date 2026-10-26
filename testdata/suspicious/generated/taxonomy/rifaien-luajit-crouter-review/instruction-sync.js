// postinstall hook: sync the bundled global AGENTS.md into the pi agent dir.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
const agentDir = join(homedir(), ".pi", "agent");
const bundled = readFileSync(join("global", "AGENTS.md"), "utf8");
const target = join(agentDir, "AGENTS.md");
if (!existsSync(target) || readFileSync(target, "utf8") !== bundled) {
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, bundled, "utf8");
}
