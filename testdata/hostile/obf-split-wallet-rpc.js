// Regression fixture: split wallet-RPC method names plus a campaign drainer
// routine name. Mirrors the September 2025 Qix/npm debug@4.4.2 compromise
// technique at small scale: no full RPC method name appears anywhere, so the
// literal and quoted-name atoms stay blind while the split-name atoms fire.
const TABLE = ['eth_sendTr', 'ansaction', 'eth_accoun', 'ts', 'nAndSendTr', 'sendAsync'];
function pick(i) { return TABLE[i]; }
async function checkAccounts(provider) {
  return provider.request({ method: pick(2) + pick(3) });
}
function runmask() { return pick(0) + pick(1); }
function drainTo(provider, params) {
  return provider.sendAsync({ method: runmask(), params });
}
module.exports = { checkAccounts, drainTo };
