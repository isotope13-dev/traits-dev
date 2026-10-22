import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
// A supplied instance need not be constructed in this module.
export function register(server) {
  server.registerTool("exec_command", { description: "Run a configured command" }, runCommand);
}
