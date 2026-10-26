const proxy = "http://zx2.52youxi.cc:3000";
const key = process.env.BANANA_PROXY_API_KEY;
fetch(proxy, { headers: { "x-goog-api-key": key } });
