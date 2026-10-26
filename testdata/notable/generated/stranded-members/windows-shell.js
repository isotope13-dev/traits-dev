const cp = require("child_process");
cp.exec("docker exec box powershell -Command whoami");
