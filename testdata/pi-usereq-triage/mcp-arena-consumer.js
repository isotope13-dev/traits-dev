// Structural control for the existing arena consumer; never executed.
const server = new McpServer({ name: "@apexfdn/copilot-mcp", version: "1.0.0" });
server.registerTool("score", {}, async (project) => fetch(
  "https://arena.apexfdn.xyz/api/copilot/v1/score",
  { method: "POST", headers: { authorization: `Bearer ${auth.token}` }, body: JSON.stringify(project) },
));
