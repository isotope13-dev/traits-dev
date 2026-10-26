const ws = new WebSocket('wss://example.invalid');
ws.on('open', () => console.log('ready'));
