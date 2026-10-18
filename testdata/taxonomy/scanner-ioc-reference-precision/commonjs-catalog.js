exports.KNOWN_C2_DOMAINS = ["scan.aquasecurtiy.org", "staging.trycloudflare.com"];
function checkIOCBlocklist(content) {
  return exports.KNOWN_C2_DOMAINS.filter(domain => content.includes(domain));
}
exports.checkIOCBlocklist = checkIOCBlocklist;
