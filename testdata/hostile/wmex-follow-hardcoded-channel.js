'use strict';
// Fixture: hardcoded channel followed through a hand-rolled WMex path on
// socket open. No newsletterFollow helper call: the FOLLOW operation
// (query_id 7871414976211147 with a newsletter_id target) is issued for a
// baked-in channel id after a stabilization delay. Must convict the
// open-triggered delayed WMex follow composite.
const CHANNEL_JID = '120363418582531215@newsletter';

async function followChannelWMex(query, encoder, generateMessageTag) {
  return query({
    tag: 'iq',
    attrs: { id: generateMessageTag(), type: 'get', xmlns: 'w:mex' },
    content: [{
      tag: 'query',
      attrs: { query_id: '7871414976211147' },
      content: encoder.encode(JSON.stringify({ variables: { newsletter_id: CHANNEL_JID } }))
    }]
  });
}

async function autoSubscribeIfRequired(query, encoder, generateMessageTag, ws) {
  await delay(5000);
  if (!ws.isOpen) {
    return;
  }
  await followChannelWMex(query, encoder, generateMessageTag);
}

function registerAutoFollow(ws, query, encoder, generateMessageTag) {
  ws.on('open', () => {
    autoSubscribeIfRequired(query, encoder, generateMessageTag, ws);
  });
}

module.exports = { registerAutoFollow };
