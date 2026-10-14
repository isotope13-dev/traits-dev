// Harvester control: walks AI assistant config directories repeatedly and
// targets credential/key file kinds. Must keep firing the secret-harvest
// verdict: directory cluster plus repeated reads plus credential-file
// targeting is two distinct collection roles.
const fs = require("node:fs");
const path = require("node:path");

const AI_DIRS = [".claude", ".codex", ".cursor"];
const WANT = [".pem", ".ppk", "conn.rdp"];

function loot(home) {
  const found = [];
  for (const d of AI_DIRS) {
    const dir = path.join(home, d);
    let entries = [];
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const ent of entries) {
      const full = path.join(dir, ent.name);
      if (ent.isDirectory()) {
        const sub = fs.readdirSync(full, { withFileTypes: true });
        for (const s of sub) {
          if (s.isDirectory()) continue;
          if (WANT.some((w) => s.name.endsWith(w))) {
            found.push(path.join(full, s.name));
          }
        }
      } else if (WANT.some((w) => ent.name.endsWith(w))) {
        found.push(full);
      }
    }
  }
  return found;
}

module.exports = { loot };
