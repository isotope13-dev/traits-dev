// Copies another app's Chromium-style cookie database and reads the session
// cookies for one host from the copy.
const fs = require("fs");
const os = require("os");
const path = require("path");
const { DatabaseSync } = require("node:sqlite");

const src = path.join(os.homedir(), ".config", "Example App", "Partitions", "account", "Network", "Cookies");
const tmp = path.join(os.tmpdir(), "example-cookies-copy.db");
fs.copyFileSync(src, tmp);

const db = new DatabaseSync(tmp, { readOnly: true });
const rows = db.prepare("SELECT name, value FROM cookies WHERE host_key = ?").all(".example.test");
module.exports = Object.fromEntries(rows.map((r) => [r.name, r.value]));
