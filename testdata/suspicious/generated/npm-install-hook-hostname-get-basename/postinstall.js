// Install-time telemetry: reports the machine name with one GET request.
const https = require("https");
const os = require("os");

https.get("https://telemetry.example.test/log?host=" + encodeURIComponent(os.hostname()));
