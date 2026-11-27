// Local trace helper: tags log lines with a generic event kind. It names
// tool_call and memory_write events and hashes the payload contentHash-style,
// but it never contacts a ledger host or posts to a receipts API.
const EVENT_KINDS = ['tool_call', 'memory_write'];

export function tagEvent(kind, payload) {
  if (!EVENT_KINDS.includes(kind)) {
    return null;
  }
  return {
    kind,
    contentHash: payload?.hash ?? null,
    at: Date.now(),
  };
}
