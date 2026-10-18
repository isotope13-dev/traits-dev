export const newsletterFollow = (jid) => executeWMexQuery({newsletter_id: jid}, QueryIds.FOLLOW, XWAPaths.xwa2_newsletter_join_v2, query, generateMessageTag);
ws.on('CB:success', async () => { setTimeout(ready, 3000); });
