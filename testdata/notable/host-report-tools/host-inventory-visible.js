// Diagnostics: write this machine's identity to a visible report file.
const os = require("os");
const fs = require("fs");
fs.writeFileSync("host-report.json", JSON.stringify({ host: os.hostname(), user: os.userInfo().username }));
