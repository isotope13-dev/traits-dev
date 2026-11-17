const endpoint = "https://service.example/mcp/sse";
const response = await fetch(endpoint, { headers: { Accept: "text/event-stream" } });
for await (const event of response.body) consume(event);
