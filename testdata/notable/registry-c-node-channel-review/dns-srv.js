const {execFile} = require("child_process");
execFile("nslookup", ["-type=SRV", "_service._tcp.example.org"], () => {});
