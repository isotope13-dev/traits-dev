const endpoint = "https://relay.ngrok-free.dev/mcp/sse";
async function bridge() {
  const response = await fetch(endpoint, { headers: { Accept: "text/event-stream" } });
  const reader = response.body.getReader();
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    process.stdout.write(new TextDecoder().decode(value));
  }
  process.stdin.on("data", async chunk => {
    await fetch(endpoint, { method: "POST", body: chunk });
  });
}
bridge();
