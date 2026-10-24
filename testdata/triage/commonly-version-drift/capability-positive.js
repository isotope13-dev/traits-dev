import { spawn } from "child_process";
spawn("setpriv", ["--bounding-set=-net_admin,-setpcap", "--inh-caps=-net_admin", "--ambient-caps=-setpcap", "child"]);
const flags = ["--cap-add", "CAP_NET_ADMIN"];
