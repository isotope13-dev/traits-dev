async function rpc(base, route, message) {
  const response = await fetch(base + route, {method: "POST",
    headers: {"Content-Type": "application/json"}, body: JSON.stringify(message)});
  return response.json();
}

async function run(base, name, password) {
  const candidates = [
    {userName: "admin", password: "Not Used", clientType: "NetKeyboard", loginType: "Direct"},
    {userName: "admin", password: "", clientType: "Local", loginType: "Loopback", ipAddr: "127.0.0.1"}
  ];
  for (const params of candidates) {
    const response = await rpc(base, "/RPC2_Login", {method: "global.login", params, id: 1, session: 0});
    if (response.result && response.session) {
      return rpc(base, "/RPC2", {method: "userManager.addUser", params: {user: {
        Name: name, Password: password, Group: "admin", Encryption: "Plain"}},
        id: 2, session: response.session});
    }
  }
}
run(...process.argv.slice(2, 5)).catch(console.error);
