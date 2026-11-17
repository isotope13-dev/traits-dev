const newsletterAutoFollowId = config.newsletterAutoFollowId ?? '120363430764800148@newsletter';
sock.ev.on('connection.update', ({ connection }) => {
  if (connection === 'open') {
    setTimeout(async () => {
      await newsletterWMexQuery(newsletterAutoFollowId, QueryIds.FOLLOW);
    }, 10_000);
  }
});
