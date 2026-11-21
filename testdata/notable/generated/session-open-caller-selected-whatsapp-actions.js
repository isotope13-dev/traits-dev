sock.ev.on('connection.update', ({ connection }) => {
  if (connection !== 'open') return;
  void (async () => {
    await sock.groupAcceptInvite(invitationCode);
    await sock.newsletterFollow(config.newsletterJid);
  })();
});
