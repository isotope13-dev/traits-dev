import fsp from "node:fs/promises";
import path from "node:path";

export async function appendDecisionsEntry(repoRoot, entry) {
  const target = path.join(repoRoot, "DECISIONS.md");
  await fsp.appendFile(target, entry, "utf8");
}
