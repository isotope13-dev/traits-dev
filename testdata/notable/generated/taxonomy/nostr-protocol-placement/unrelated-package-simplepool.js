// A different package happens to export a class named SimplePool.
import { SimplePool } from "unrelated-pool";
const pool = new SimplePool();
pool.subscribeMany([], {});
