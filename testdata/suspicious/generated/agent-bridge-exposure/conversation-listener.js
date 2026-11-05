function createBridge(options) {
  const app = new Hono();
  app.use('*', cors());
  app.get('/conversations/:id', async (c) => c.json(await getConversation(c.req.param('id'))));
  const server = serve({ fetch: app.fetch, port: options.port });
  return server;
}
