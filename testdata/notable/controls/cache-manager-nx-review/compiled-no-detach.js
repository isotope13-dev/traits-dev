const cp = require("child_process");
(0, cp.spawn)("node", ["worker.js"], {detached: false});
