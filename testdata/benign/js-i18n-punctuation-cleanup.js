// i18n text cleaning: strip fullwidth/CJK punctuation and Chinese
// enumeration marks from token edges before matching.
function cleanToken(t) {
  return t
    .replace(/^[`'"(]+|[`'"),.;:，。；：]+$/gu, "")
    .replace(/^(?:[一二三123][、.．]\s*)/, "");
}

function stripHeadingMarks(t) {
  return t.replace(/^#{1,6}\s*/, "").replace(/[：:]\s*$/, "").trim();
}

module.exports = { cleanToken, stripHeadingMarks };
