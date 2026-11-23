const fs = require("fs");
const keys = fs.readFileSync("C:/Users/p/.openclaw/workspace/project/12-D.txt", "utf8");
const n = { apiKey: keys.split("\n").find(s => s.startsWith("sk-")) };
const s = {};
s.Authorization="Bearer "+n.apiKey;
fetch("https://8888ok.cc/v1" + "/chat/completions", {
  method: "POST", headers: s, body: JSON.stringify({ messages: [] })
});
