const fs = require("fs");
const https = require("https");
// Inspect Bitcoin data and secure a local cache; no execution.
https.get("https://blockstream.info/testnet/api/address/demo/txs", res => {
  res.on("data", chunk => console.log(chunk.toString()));
});
const opcode = "op_return";
fs.chmodSync("cache.json", 0o700);
