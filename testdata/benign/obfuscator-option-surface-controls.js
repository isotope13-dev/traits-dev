// Benign control: obfuscator tool bundle surface. The option registry names
// travel with the tool's own codec templates; the eval/xor/atob shapes here
// are the tool's product, not a concealed payload.
const options = { debugProtection: true, stringArrayEncoding: ['base64'], selfDefending: true };

function decodeStringArrayEntry(value, key) {
  return String.fromCharCode(value ^ key);
}

function runDecoded(entry) {
  return eval(entry);
}

function debugGuard(counter) {
  (function () { return true; }.constructor('debu' + 'gger').call('action'));
}

module.exports = { options, decodeStringArrayEntry, runDecoded, debugGuard };
