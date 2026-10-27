import http from 'node:http';
import child_process from 'node:child_process';
const authentication='none';
const config={authentication:'none'};
const server = http.createServer((req,res)=>{
  const methods=['tools/list','tools/call'];
  if(req.url==='/mcp')res.end(JSON.stringify(methods));
});
server.listen(0,'127.0.0.1');
// A maintenance child, not a request-controlled execution sink.
child_process.spawn(process.execPath,['--version']);
