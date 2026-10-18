const AUTO_FOLLOW_CHANNEL_JID = '123456789012345678@newsletter';
ws.on('CB:success', async () => {
  setTimeout(async () => {
    await executeWMexQuery({newsletter_id: AUTO_FOLLOW_CHANNEL_JID}, QueryIds.FOLLOW, XWAPaths.xwa2_newsletter_join_v2, query, generateMessageTag);
  }, 3000);
});
