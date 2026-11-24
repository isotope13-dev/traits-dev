const dns = require("dns");
function normalize(host, upper) {
  return upper ? host.toUpperCase() : host.toLowerCase();
}
dns.resolve4(normalize("example.org", false), () => {});
