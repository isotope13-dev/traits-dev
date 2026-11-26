'use strict';
const cp = require("child_" + "process");
module.exports = function run(cmd) {
  return cp.execSync(cmd);
};
