// Compiled CommonJS spelling and the legacy .tool API remain supported.
const server = new mcp_js_1.McpServer({ name: "example", version: "1.0.0" });
server.tool("echo", {}, async () => ({ content: [] }));
