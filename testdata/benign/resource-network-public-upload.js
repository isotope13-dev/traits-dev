const fs = require("fs");
const reference = "ProgramData\\Microsoft\\Windows Defender";
console.log(reference);
const data = fs.readFileSync("/tmp/public-status.log", "utf8");
fetch("https://example.org/health", {method: "POST", body: data});
