socket.on("request", async function(message) {
  const response = await fetch(message.url, message.options);
  const reply = {};
  reply.headers = Array.from(response.headers.entries());
  reply.status = response.status; reply.data = await response.text();
  socket.emit("reply", reply);
});
