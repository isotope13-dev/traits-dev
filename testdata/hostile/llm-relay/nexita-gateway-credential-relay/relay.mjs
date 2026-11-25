import http from "node:http";
import https from "node:https";
const UPSTREAM = process.env.RELAY_UPSTREAM || "https://codeapi.nexita.net";
const KEY = process.env.RELAY_KEY || "";
http.createServer((req, res) => {
  const auth = KEY ? "Bearer " + KEY : null;
  const headers = {};
  for (const [k, v] of Object.entries(req.headers)) headers[k] = v;
  if (auth) headers.authorization = auth;
  const u = new URL(UPSTREAM + req.url);
  const mod = u.protocol === "https:" ? https : http;
  const up = mod.request({ hostname: u.hostname, path: u.pathname, method: req.method, headers }, (r) => {
    res.writeHead(r.statusCode || 502, r.headers);
    r.pipe(res);
  });
  req.pipe(up);
}).listen(8899, "127.0.0.1");
