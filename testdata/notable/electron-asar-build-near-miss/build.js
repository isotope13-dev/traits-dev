
const fs = require("fs");
const path = require("path");
const asar = require("@electron/asar");

async function packageRelease(buildDir, outAsar) {
  const pkgPath = path.join(buildDir, "package.json");
  const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
  pkg.main = "dist/main.js";
  fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2));
  fs.copyFileSync(path.join(__dirname, "LICENSE"), path.join(buildDir, "LICENSE"));
  await asar.createPackageWithOptions(buildDir, outAsar, {
    unpackDir: "node_modules/@koromix/koffi-win32-x64"
  });
}
