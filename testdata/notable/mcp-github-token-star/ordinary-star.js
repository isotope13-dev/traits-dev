import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
const service = new McpServer({name: 'example', version: '1'});
service.registerTool('example', {description: 'Star a repository with the token you provide', inputSchema: {}}, async () => ({}));
async function star(credential) {
  await fetch(`https://api.github.com/user/starred/${target}`, {
    method: 'PUT',
    headers: {Authorization: `token ${credential}`}
  });
}
