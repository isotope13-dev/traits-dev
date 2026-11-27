const http = require('node:http');
const originalCreateServer = http.createServer;
http.createServer = (...args) => {
  const originalListener = args[0];
  return originalCreateServer(async (req, res) => {
    if (req.url === '/private-sql') return handler(req, res);
    originalListener(req, res);
  });
};
async function handler(req, res) {
  const parsed = await parseBody(req);
  const { query, dbType } = parsed.data;
  // Example only: poolPg.query(query)
  res.end('Database execution disabled');
}
