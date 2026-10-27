const {spawn} = require("child_process");
spawn("node", ["worker.js"], {detached: true, stdio: "ignore"}).unref();
