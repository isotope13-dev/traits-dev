// Diagnostics helper. Older releases pinged x.oob.example-collector.com;
// that was removed. This file now only confirms the local resolver works
// before the native build step and prints a warning when it does not.
const dns = require("dns");
dns.lookup("localhost", (err) => { if (err) console.warn("resolver unavailable"); });
