const https = require("https");

https.get("https://updates.example.invalid/status", (response) => {
  response.resume();
});
