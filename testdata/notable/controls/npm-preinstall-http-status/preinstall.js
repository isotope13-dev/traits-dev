const http = require("http");

http.get("http://updates.example.invalid/status", (response) => {
  response.on("data", (chunk) => process.stdout.write(chunk));
});
