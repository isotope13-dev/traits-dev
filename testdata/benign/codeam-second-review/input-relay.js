sock.on('data', (data) => { child.stdin.write(data); });
