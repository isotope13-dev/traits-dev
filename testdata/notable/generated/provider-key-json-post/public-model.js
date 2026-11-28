async function storeProviderKey(apiKey) {
  const response = await fetch("https://vault.example.test/provider", {
    method: "POST",
    body: JSON.stringify({ model: apiKey })
  });
  return response.ok;
}
