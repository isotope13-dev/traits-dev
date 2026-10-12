// Benign control: Node fs.open with a mode flag shares the open(path, flag)
// shape but opens a file descriptor, not a URL in a named window. Must NOT
// fire open-computed-url-named-target.
import { open } from "node:fs/promises";
export async function appendLine(port, packet) {
  const handle = await open(port, "w");
  try {
    await handle.writeFile(packet, "utf8");
  } finally {
    await handle.close();
  }
}
