// unread badge: counts unread items only, never posts anything
async function badge() {
  const r = await fetch("https://mail.google.com/mail/u/0/feed/atom", { credentials: "include" });
  const t = await r.text();
  const n = (t.match(/<fullcount>(\d+)<\/fullcount>/) || [])[1];
  chrome.action.setBadgeText({ text: n || "" });
}
chrome.alarms.create("b", { periodInMinutes: 5 });
chrome.alarms.onAlarm.addListener(badge);
