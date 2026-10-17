// Decoded-payload execution: runs whatever the base64 blob decodes to.
function load(blob) {
  return eval(atob(blob));
}
module.exports = { load: load };
