import path from "node:path";
import fsp from "node:fs/promises";

export async function ensureOnPath() {
  const home = process.env.HOME ?? "";
  const target = path.join(home, ".zshrc");
  await fsp.appendFile(target, '\nexport PATH="$HOME/.local/bin:$PATH"\n', "utf8");
}
