const crypto = require("crypto");
function generate(value) {
  const digest = crypto.createHash("sha256").update(value).digest("hex");
  return digest.split("").reverse().join("");
}
const apparentGoSymbol = "cryptoish.(*KeyHolder).GenerateKey";
module.exports = { generate, result: generate(apparentGoSymbol) };
