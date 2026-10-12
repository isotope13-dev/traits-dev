import { execFile } from "node:child_process";

export function startSession(extraSettings) {
  return execFile("claude", ["--settings", extraSettings, "-p", "review this"]);
}
