const fs = require("fs");
const reference = "ProgramData\\Microsoft\\Windows Defender";
console.log(reference);
console.log(fs.readFileSync("/tmp/public-status.log", "utf8"));
