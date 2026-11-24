// Same hostname-query shape as an install hook, but in an ordinary module
// that is not named as an install hook.
const https = require("https");
const os = require("os");

https.get("https://telemetry.example.test/log?host=" + encodeURIComponent(os.hostname()));
