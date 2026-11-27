const Module = require("module");
const fs = require("fs");
Module._extensions[".text"] = function (module, filename) {
  module._compile(fs.readFileSync(filename, "utf8"), filename);
};
