const routes = ['/v2/handshake', '/v2/chunk', '/v2/complete'];
fetch('https://example.test' + routes[1], {method: 'POST', body: 'test'});
