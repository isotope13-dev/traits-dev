const fs = require("fs");
const http = require("http");
const file = fs.readFileSync("/tmp/example.txt", "utf8").trim();
const req = http.request({ hostname:"127.0.0.1", method:"PUT" });
const payload = JSON.stringify({data:"constant"});
req.write(payload);
req.end();
