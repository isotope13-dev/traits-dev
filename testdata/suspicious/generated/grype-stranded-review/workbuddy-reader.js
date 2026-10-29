const fs = require("fs");
const {safeStorage} = require("electron");
const text = fs.readFileSync("workbuddy-desktop.info", "utf8");
const record = JSON.parse(text);
const accessToken = safeStorage.decryptString(Buffer.from(record.accessToken, "base64"));
