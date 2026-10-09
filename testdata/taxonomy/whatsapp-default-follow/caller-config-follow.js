export function socket(config, ev) {
  ev.on('connection.update', ({connection}) => {
    if (connection !== 'open') return;
    for (const jid of config.autoFollowChannels || []) {
      newsletterWMexQuery(jid, QueryIds.FOLLOW);
    }
  });
}
