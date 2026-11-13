// Minimal Bun socket and HTTP server capability, shaped like a compiled
// single-file Bun helper's embedded module (loopback only).
const server = Bun.listen({
  hostname: "127.0.0.1",
  port: 7601,
  socket: {
    open(socket) { socket.write("ready\n"); },
    data(socket, chunk) { socket.write(chunk); },
  },
});
const http = Bun.serve({
  hostname: "127.0.0.1",
  port: 7602,
  fetch(request) { return new Response("ok"); },
});
