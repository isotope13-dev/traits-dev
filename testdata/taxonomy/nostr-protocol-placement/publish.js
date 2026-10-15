import { SimplePool } from "nostr-tools";
const pool = new SimplePool();
pool.publish("wss://relay.example", { kind: 1, content: "" });
