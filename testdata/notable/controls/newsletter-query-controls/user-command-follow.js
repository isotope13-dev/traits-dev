// Channel admin helper: follows a channel only when the operator invokes
// the follow command with an explicit JID. No remote list, no timer.
async function followChannel(query, generateMessageTag, encoder, jid) {
  if (!/^\d{10,20}@newsletter$/.test(jid)) {
    throw new TypeError('followChannel: explicit channel JID required');
  }
  return query({
    tag: 'iq',
    attrs: { id: generateMessageTag(), type: 'get', xmlns: 'w:mex', to: '@s.whatsapp.net' },
    content: [{
      tag: 'query',
      attrs: { query_id: '7871414976211147' },
      content: encoder.encode(JSON.stringify({ variables: { newsletter_id: jid } })),
    }],
  });
}

module.exports = { followChannel };
