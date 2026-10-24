const res = await fetch(url, { method: 'PROPFIND', headers: { 'Depth': '1' } });
const nodes = xml.select('//d:href');
for (const node of nodes) {
  const text = Buffer.from(node.name.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8');
  use(text);
}
