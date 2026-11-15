const http = require("http");
http.request({ hostname: "status.example.com", port: 80, path: "/health", method: "GET" }).end();
