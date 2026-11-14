const dns = require("dns");

dns.resolve4("registry.npmjs.org", (error, addresses) => {
  if (!error) console.log(addresses[0]);
});
