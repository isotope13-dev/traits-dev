// XML parser option: keep text nodes for mixed content.
const parserOptions = {
  alwaysCreateTextNode: true,
  trimValues: false
};
// See https://developer.mozilla.org/en-US/docs/Web/API/Document/createTextNode
function makeText(doc, value) {
  return doc.createTextNode(value);
}
module.exports = { parserOptions, makeText };
