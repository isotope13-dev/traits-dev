const https = require("https");
https.get("https://updates.example.com/health", () => {}).on("error", () => {});
