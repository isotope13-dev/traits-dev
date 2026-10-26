// Minimal unauthenticated MCP command service (hand-rolled JSON-RPC shape):
// advertises tools over tools/list, dispatches the caller's choice over
// tools/call, runs it in a child process, listens on HTTP, and declares
// no authentication. Must trip mcp-noauth-http-command-service.
import http from 'node:http';
import { spawn } from 'node:child_process';

const tools = [
  { name: 'run_command', description: 'Run an executable with exact arguments.', securitySchemes: [{ type: 'noauth' }] },
  { name: 'server_info', description: 'Inspect this installation.', securitySchemes: [{ type: 'noauth' }] },
];

function callTool(name, args) {
  if (name === 'run_command') {
    const child = spawn(args.executable, args.args || [], { shell: false });
    return child;
  }
  if (name === 'server_info') return { product: 'example', authentication: 'none' };
  throw new Error('Unknown tool');
}

const server = http.createServer((req, res) => {
  let body = '';
  req.on('data', (chunk) => { body += chunk; });
  req.on('end', () => {
    const message = JSON.parse(body);
    if (message.method === 'tools/list') {
      res.end(JSON.stringify({ result: { tools } }));
    } else if (message.method === 'tools/call') {
      const result = callTool(message.params.name, message.params.arguments || {});
      res.end(JSON.stringify({ result: { started: !!result } }));
    } else {
      res.end(JSON.stringify({ error: 'Unknown method' }));
    }
  });
});
server.listen(8471, '127.0.0.1');
