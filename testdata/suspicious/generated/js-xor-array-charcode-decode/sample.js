// Decodes a package-local repository name from an XOR-keyed byte table.
const _k = 169;
function _d(e) { return e.map(b => b ^ _k).map(b => String.fromCharCode(b)).join(""); }
const REPO = _d([236,209,200,196,217,197,204,132,230,219,206,134,221,198,198,197]);
module.exports = { REPO };
