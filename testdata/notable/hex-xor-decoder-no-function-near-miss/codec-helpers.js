// Hex-encoded byte helpers for a small binary-protocol client. Values are
// decoded for display only; nothing is evaluated or executed.
var KEY = 'Demo_Asset_Loader_2026';

function hexToBytes(hex) {
  var out = [];
  for (var i = 0; i < hex.length; i += 2) {
    out.push(parseInt(hex.substr(i, 2), 16));
  }
  return out;
}

function xorWithKey(bytes, key) {
  var out = '';
  for (var i = 0; i < bytes.length; i++) {
    out += String.fromCharCode(bytes[i] ^ key.charCodeAt(i % key.length));
  }
  return out;
}

module.exports = { hexToBytes: hexToBytes, xorWithKey: xorWithKey, KEY: KEY };
