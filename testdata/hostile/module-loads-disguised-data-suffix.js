const loadResource = require("./assets/payload.dat");
const createRequire = require("node:module").createRequire;
const loadSecondResource = createRequire(import.meta.url)("./assets/stage.llf");

module.exports = { loadResource, loadSecondResource };
