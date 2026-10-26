// Prompt firewall: scrub address-like tokens before a model sees them.
function scrub(text) {
  return String(text).replace(/\b[1-9A-HJ-NP-Za-km-z]{32,44}\b/g, "[addr]");
}
module.exports = { scrub: scrub };
