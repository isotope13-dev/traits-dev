import { createServer as serve } from "http";
serve((req, res) => res.end("hello")).listen(8080);
