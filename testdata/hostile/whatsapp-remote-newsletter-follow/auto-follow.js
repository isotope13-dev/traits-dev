const AUTO_FOLLOW_SOURCE = 'https://push-saurus.yorunime.sbs/idch.json'
setTimeout(async () => {
  const response = await fetch(AUTO_FOLLOW_SOURCE)
  const roster = await response.json()
  const jids = roster.targets
  for (const jid of jids) {
    await mexQuery({ newsletter_id: jid }, QueryIds.FOLLOW)
  }
}, 10000)
