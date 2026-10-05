const updates = new WebSocket('wss://updates.example.invalid/feed');
updates.onmessage = function(packet) {
  document.querySelector('#status').textContent = JSON.parse(packet.data).text;
};
