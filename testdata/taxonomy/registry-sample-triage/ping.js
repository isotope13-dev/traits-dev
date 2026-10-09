const cp = require("child_process");
cp.exec(`ping ${host}`);
cp.execSync("ping " + host);
