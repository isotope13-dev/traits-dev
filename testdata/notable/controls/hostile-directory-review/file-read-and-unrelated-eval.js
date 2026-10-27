const fs = require("fs");
const path = require("path");
const template = fs.readFileSync(path.join(__dirname, "template.txt"), "utf8");
function evaluateUserExpression(expression) {
  return eval(String(expression));
}
console.log(template);
