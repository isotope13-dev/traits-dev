// Local dev-dashboard client: polls its own loopback UI server route.
// A lone /api/status reference with no report/update paths and no loader
// domain is ordinary dashboard surface, not a loader protocol.
export const pollSwarmStatus = async (db, cwd) => {
  const routes = {
    '/api/status': () => ({ ok: true, db, cwd }),
  };
  const handler = routes['/api/status'];
  return handler();
};
