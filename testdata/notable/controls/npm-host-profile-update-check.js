const dns = require("dns");
const https = require("https");

dns.resolve4("updates.example.invalid", () => {});
https.get("https://updates.example.invalid/status", (response) => {
  response.resume();
});
