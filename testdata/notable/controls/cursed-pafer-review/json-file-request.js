const fs = require("fs");
const http = require("http");
const text = fs.readFileSync("/tmp/example.txt", "utf8").trim();
const req = http.request({ hostname:"127.0.0.1", method:"PUT" });
const body = JSON.stringify({data:text});
req.write(body);
req.end();
