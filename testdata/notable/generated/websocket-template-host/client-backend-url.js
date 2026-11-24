// Client builds the URL of its own configured backend; no remote host is named.
export function buildWsUrl (host, port, token, id) {
  return `ws://${host}:${port}/terminals/${id}?token=${token}`
}
