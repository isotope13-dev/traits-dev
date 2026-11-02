// Benign control: fixed client-side verify command, nothing server-driven.
// Never executed; structural control only.
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
const server = new McpServer({ name: 'example-helper', version: '1.0.0' });
server.registerTool('helper_score', {}, async () => ({ content: [{ type: 'text', text: 'ok' }] }));
export function verifyHelp(code) {
  return [
    'Connection needs to be re-verified before continuing.',
    '',
    'Run this in your terminal to refresh your connection:',
    '',
    `  npx example-helper verify ${code}`,
  ].join('\n');
}
