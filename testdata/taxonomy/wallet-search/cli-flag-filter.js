import { resolve } from "node:path";

const configPath = resolve(".tool/settings.json");
const extraPath = resolve(".tool/extra.json");

export function run(args) {
  const dryRun = args.includes("--dry-run");
  const index = args.indexOf("--target");
  const target = index >= 0 && args[index + 1] ? args[index + 1] : null;
  return { configPath, extraPath, dryRun, target };
}
