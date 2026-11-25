'use strict';
// Synthetic regression fixture: obfuscator-shaped loader with a hidden detached child. Inert.
var _0x3a1f = ['detached-name', 'windowsHide-name', '\x73\x70\x61\x77\x6e', '\x2d', '\x73\x74\x64\x69\x6f', '\x70\x69\x70\x65'];
(function (_0x5b2c, _0x4d1e) {
  var _0x1f8a = function (_0x2e3f) {
    while (--_0x2e3f) {
      _0x5b2c['push'](_0x5b2c['shift']());
    }
  };
  _0x1f8a(++_0x4d1e);
}(_0x3a1f, 0x1a3));
var _0x2a7d = function (_0x1c9e) {
  _0x1c9e = _0x1c9e - 0x0;
  return _0x3a1f[_0x1c9e];
};
var _0x9e1b = function (_0x7a3c, _0x6d2f) {
  var _0x8c4e = 0x0;
  while (!![]) {
    try {
      var _0x3f1d = parseInt(_0x7a3c) / 0x1 + -parseInt(_0x6d2f) / 0x2;
      if (_0x3f1d === 0x0) { break; } else { _0x8c4e++; }
    } catch (_0x4b2a) {
      _0x8c4e++;
    }
  }
  return _0x8c4e;
};
var cp = require('\x63\x68\x69\x6c\x64\x5f\x70\x72\x6f\x63\x65\x73\x73');
var child = cp[_0x2a7d(0x2)](process.execPath, [_0x2a7d(0x3)], {
  windowsHide: true,
  detached: true,
  '\x73\x74\x64\x69\x6f': ['pipe', 'pipe', 'pipe']
});
child[_0x2a7d(0x5)].end(_0x9e1b('1', '2'));
