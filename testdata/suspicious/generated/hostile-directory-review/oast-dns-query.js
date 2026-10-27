const dns = require("dns");
const destination = "probe" + ".oastify.com";
dns.lookup(destination, () => {});
