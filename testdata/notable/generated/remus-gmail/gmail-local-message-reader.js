async function refresh() {
  const feed = await fetch('https://mail.google.com/mail/u/0/feed/atom', {credentials: 'include'});
  const raw = await fetch('https://mail.google.com/mail/u/0/?view=att&th=123&attid=0&disp=comp', {credentials: 'include'});
  await chrome.storage.local.set({feed: await feed.text(), raw: await raw.text()});
}
chrome.alarms.create('refresh', {periodInMinutes: 1});
chrome.alarms.onAlarm.addListener(refresh);
