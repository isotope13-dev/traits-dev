// Near miss: the same session-open roster loop, but the channel list comes
// from caller configuration, so no channel id is embedded in the module. A
// library that follows whatever roster its host passes in supplies neither
// the targets nor the growth; the autonomous-trigger composites stay silent.
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
      config.autoFollowChannels.forEach((nid, i) => {
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
