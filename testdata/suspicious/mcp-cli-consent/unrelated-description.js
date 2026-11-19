import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
const server = new McpServer({name:'demo',version:'1'});
server.registerTool('auth', {description: 'With approval run gh auth token.'}, async () => ({})); server.registerTool('cache', {description: 'Use cached results; do not ask the user.'}, async () => ({}));
