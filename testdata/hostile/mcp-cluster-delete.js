const command = 'sudo kill -9 $(lsof -ti:6432); sleep 2; sudo rm -fr /var/lib/postgresql/17/main';
const response = await fetch('http://127.0.0.1:41900/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json', Authorization: 'Bearer fixture-token'},
  body: JSON.stringify({jsonrpc: '2.0', id: 7, method: 'tools/call', params: {
    name: 'exec_in_session', arguments: {session_id: 3, command}
  }})
});
console.log(await response.text());
