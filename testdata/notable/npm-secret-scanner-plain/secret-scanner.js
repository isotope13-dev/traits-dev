// Regression control: an ordinary secret scanner implementation. Same
// catalog, RegExp and directory-walk plumbing as the padded positive, but no
// whitespace concealment, so the secret-sweep composite must not fire and
// the file stays notable.
const SECRET_PATTERNS = [
  [/[A-Za-z0-9+/]{40,}/, "generic-b64"],
  [/sk-[A-Za-z0-9-]{16,}/, "api-key"],
  [/xox[bpor]-[0-9A-Za-z-]{10,}/, "slack"],
];
const { readdir, readFile } = require("fs");
const walk = async (dir, report) => {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const p = dir + "/" + entry.name;
    if (entry.isDirectory()) await walk(p, report);
    else {
      const t = await readFile(p, "utf8");
      const a = new RegExp(t.slice(0, 4), "g");
      const b = new RegExp(p.slice(0, 4), "g");
      const c = new RegExp(entry.name.slice(0, 4), "g");
      if (a.test(t) || b.test(t) || c.test(t)) report(p);
    }
  }
};
walk(".", (hit) => console.log("finding", hit));
