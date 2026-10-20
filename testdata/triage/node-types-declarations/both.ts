declare module "example" { function example(): void; }
import { createServer } from "node:http";
createServer(() => {}).listen(8080);
