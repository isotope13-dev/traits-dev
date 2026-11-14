const fs = require("fs");

const packageInfo = JSON.parse(fs.readFileSync("package.json", "utf8"));
console.log(packageInfo.name, Object.keys(packageInfo.dependencies || {}));
