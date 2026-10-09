const fs = require("fs");
const entries = fs.readdirSync(dir);
for (const entry of entries) { const stat = fs.statSync(entry); result.push(stat); }
