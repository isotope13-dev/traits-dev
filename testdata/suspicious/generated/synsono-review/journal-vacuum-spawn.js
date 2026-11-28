const cp = require("node:child_process");
cp.spawnSync('journalctl', [ '--vacuum-time=1s' ], {stdio: "inherit"});
