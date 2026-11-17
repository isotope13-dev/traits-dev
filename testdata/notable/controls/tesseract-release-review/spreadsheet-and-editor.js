const fs = require('fs');
const xml = '<sheetData/><xdr:clientData/><ClientData ObjectType="Note"/>';
function buildTree(spans, node, offset) {
  const children = [];
  node.forEach(child => children.push(buildTree(spans, child, offset + 1)));
  return children;
}
module.exports = { xml, buildTree };
