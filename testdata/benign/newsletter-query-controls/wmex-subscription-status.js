'use strict';
// Fixture: subscription status reader. A hardcoded channel id, a socket-open
// handler and a stabilization delay are all present, but the file only
// READS subscription state and logs it: no FOLLOW operation is ever
// issued, so the open-triggered WMex follow composite must stay silent.
const CHANNEL_JID = '120363418582531215@newsletter';

async function fetchSubscriptionList(query) {
  const result = await query({
    tag: 'iq',
    attrs: { type: 'get', xmlns: 'newsletter' },
    content: [{ tag: 'list', attrs: {} }]
  });
  return result;
}

async function logSubscriptionStatus(query, ws) {
  await delay(5000);
  if (!ws.isOpen) {
    return;
  }
  const list = await fetchSubscriptionList(query);
  const found = Array.isArray(list) && list.some((n) => n.id === CHANNEL_JID);
  console.log('channel subscription status:', found ? 'subscribed' : 'absent');
}

function registerStatusCheck(ws, query) {
  ws.on('open', () => {
    logSubscriptionStatus(query, ws);
  });
}

module.exports = { registerStatusCheck };
