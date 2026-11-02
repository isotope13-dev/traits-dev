const dns = require("node:dns");
const host = "api.trusted.example";
if (host.endsWith(".trusted.example")) {
  dns.resolve4(host, (e, a) => console.log(a));
}
