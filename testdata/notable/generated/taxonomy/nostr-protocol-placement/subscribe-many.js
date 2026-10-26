import { SimplePool } from "nostr-tools";
const pool = new SimplePool();
pool.subscribeMany(["wss://relay.example"], { onevent() {} });
