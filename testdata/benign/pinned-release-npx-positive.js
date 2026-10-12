const {spawnSync} = require("child_process");
spawnSync("npx", ["-y", "@vendor/tool"]);
