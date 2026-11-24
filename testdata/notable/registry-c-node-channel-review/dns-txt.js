const {execFile} = require("child_process");
execFile("nslookup", ["-type=TXT", "example.org"], () => {});
// execFile("nslookup", ["-type=SRV", "example.org"]);
