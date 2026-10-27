const cp = require("child_process");
cp.execFile("worker", [], {"detached": !0});
