import { spawn } from "node:child_process";

export function unpack(archive, dest) {
  return new Promise((resolve) => {
    const child = spawn("tar", ["-xzf", archive, "-C", dest, "--strip-components=1"]);
    child.on("close", (code) => resolve(code));
  });
}
