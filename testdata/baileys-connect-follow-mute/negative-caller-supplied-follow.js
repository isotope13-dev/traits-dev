ev.on('connection.update', ({ connection }) => {
  if (connection === 'open') {
    logger.info('session open');
  }
});

async function followOnCommand(jid) {
  await sock.newsletterFollow(jid);
}
