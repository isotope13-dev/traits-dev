const dns = require("node:dns");
const n = "mail.evil-corp.test\x00.corp.internal";
dns.resolveTxt(n, (e, r) => console.log(r));
