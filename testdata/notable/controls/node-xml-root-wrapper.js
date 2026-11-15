const { parseSync } = require('xml-reader');
function parseFragment(input) {
  return parseSync('<root>'.concat(input, '</root>'), { parentNodes: false });
}
module.exports = parseFragment;
