element.addEventListener('change', function(event) { socket.emit('edit', event.target.value); });
