export function start(server, app) {
  server?.listen(3000);
  app.listen(3001);
}
