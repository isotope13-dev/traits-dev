import { createServer } from "node:http";
createServer((req, res) => res.end("hello")).listen(8080);
