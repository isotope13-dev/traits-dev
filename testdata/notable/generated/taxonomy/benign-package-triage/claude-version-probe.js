import { execFile } from "node:child_process";
import { promisify } from "node:util";

const run = promisify(execFile);

export async function doctor() {
  try {
    const { stdout } = await run("claude", ["--version"]);
    return stdout.trim();
  } catch {
    return null;
  }
}

export function option(args, name, fallback) {
  const index = args.indexOf(name);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

export const settingsPath = option(process.argv.slice(2), "--settings", null);
