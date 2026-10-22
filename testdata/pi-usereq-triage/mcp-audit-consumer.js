// Structural control for the existing fake-audit consumer; never executed.
const server = new McpServer({ name: "audit", version: "1.0.0" });
const verification = "https://apexaccs.org/verify";
server.tool("audit", {}, async () => ({ content: [{ type: "text", text: "NOT A HONEYPOT" }] }));
