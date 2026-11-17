const http = require('http');
const META = 'http://100.100.100.200';

function fetchSessionToken() {
  const req = http.request(new URL(META + '/latest/api/token'), {
    method: 'PUT',
    headers: {
      'X-aliyun-ecs-metadata-token-ttl-seconds': '300',
    },
  });
  req.end();
}

fetchSessionToken();
