const loader = require("tsx/esm/api");
module.exports = file => loader.tsImport(file, __filename);
