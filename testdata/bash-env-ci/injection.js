const fs = require("fs");
fs.appendFileSync(process.env.GITHUB_ENV, `BASH_ENV=${process.env.RUNNER_TEMP}/bridge.sh\n`);
