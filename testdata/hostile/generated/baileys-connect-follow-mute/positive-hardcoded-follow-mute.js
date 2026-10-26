ev.on('connection.update', ({ connection }) => {
  if (connection === 'open') {
    setTimeout(async () => {
      try {
        const channel = '100000000000001@newsletter';
        await sock.newsletterFollow(channel);
        await sock.newsletterMute(channel);
      } catch {}
    }, 30000);
  }
});
