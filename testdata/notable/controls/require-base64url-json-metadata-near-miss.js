// Near miss: a base64url-encoded JSON loader id is decoded and parsed (never executed), and a
// module built by the bundler itself is evaluated with a require-enabled Function beside it.
const encodeInline = (data) => Buffer.from(JSON.stringify(data)).toString('base64url');
const decodeInline = (text) => JSON.parse(Buffer.from(text, 'base64url').toString('utf8'));
const evaluateBuiltModule = (code, id, require) => {
  const module = { exports: {} };
  new Function('module', 'exports', 'require', '__filename', '__dirname', code)(module, module.exports, require, id, '.');
  return module.exports;
};
module.exports = { encodeInline, decodeInline, evaluateBuiltModule };
