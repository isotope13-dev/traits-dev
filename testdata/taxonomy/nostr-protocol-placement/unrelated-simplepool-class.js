// An unrelated local type happens to use the same class name as nostr-tools.
class SimplePool {
  subscribeMany() {}
}

const pool = new SimplePool();
pool.subscribeMany([], {});
