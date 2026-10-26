// Validation helpers for Ethereum addresses and transaction hashes.
// The hex-run quantifiers below are 0x-prefixed address shapes, which are
// not bare file-digest patterns.
const ETH_ADDRESS = /^0x[a-fA-F0-9]{40}$/;
const TX_HASH = /^0x[a-fA-F0-9]{64}$/;

function isAddress(text) {
  return typeof text === 'string' && ETH_ADDRESS.test(text);
}

function isTxHash(text) {
  return typeof text === 'string' && TX_HASH.test(text);
}

module.exports = { isAddress, isTxHash };
