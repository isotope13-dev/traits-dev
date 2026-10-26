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
discover().then(host => console.log(host));
