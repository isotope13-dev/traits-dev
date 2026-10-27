const dns = require("dns");
const documentation = "An example callback host is probe.oastify.com";
dns.lookup("registry.npmjs.org", () => {});
console.log(documentation);
