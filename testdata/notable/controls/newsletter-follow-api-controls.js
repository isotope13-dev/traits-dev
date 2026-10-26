// Parameterized newsletter API surface: the caller supplies the channel
// JID and invokes the follow explicitly. No connect-time trigger, no preset
// default target, no delayed dispatch.
export const newsletterFollow = async (sock, jid) => {
  return sock.query({
    tag: "iq",
    attrs: { id: sock.generateMessageTag(), type: "get", xmlns: "w:mex", to: "@s.whatsapp.net" },
    content: [{
      tag: "query",
      attrs: { query_id: "7871414976211147" },
      content: new TextEncoder().encode(JSON.stringify({ variables: { newsletter_id: jid } })),
    }],
  });
};
