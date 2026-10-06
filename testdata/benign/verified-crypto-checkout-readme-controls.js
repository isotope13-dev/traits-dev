// Benign control: crypto payment plugin readme prose scanned as script.
// "blockchain transaction" here is product vocabulary describing on-chain
// settlement, not a dead-drop payload source.
var readme = [
  'Stable tag: 1.56.55',
  'If the provider reports a payment without a blockchain transaction hash,',
  'the order is placed On Hold instead of Completed, with a clear note',
  'telling you not to ship until funds are confirmed in your wallet.'
].join('\n');

module.exports = { readme };
