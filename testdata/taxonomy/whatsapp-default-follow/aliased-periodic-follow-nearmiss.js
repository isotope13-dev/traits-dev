export function makeNewsletterSocket(sock, ev, config) {
  const followChannel = async (jid) => {
    await wmex({ newsletter_id: jid }, QueryIds.FOLLOW, XWAPaths.xwa2_newsletter_join_v2);
  };
  ev.on('connection.update', async ({ connection }) => {
    if (connection !== 'open') return;
    for (const jid of config.followChannels || []) {
      await followChannel(jid);
    }
  });
}
