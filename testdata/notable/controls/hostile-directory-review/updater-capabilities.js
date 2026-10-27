const { execSync, spawnSync } = require("child_process");
async function readVersion() {
  return (await fetch("https://example.org/version")).text();
}
function update() {
  execSync("npm install -g example-cli --force --registry=https://registry.npmjs.org");
  spawnSync("example-cli", process.argv.slice(2), { stdio: "inherit" });
}
