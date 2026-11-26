// Vendor installer helper (regression fixture, synthetic).
const { execFile } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

async function runInstaller(base, dir) {
  const res = await fetch(base + "/install.ps1");
  if (!res.ok) throw new Error("HTTP " + res.status);
  const file = path.join(os.tmpdir(), "install.ps1");
  fs.writeFileSync(file, await res.text());
  execFile("powershell.exe", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", file, "-Dir", dir]);
}

module.exports = { runInstaller };
