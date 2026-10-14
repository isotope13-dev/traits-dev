'use strict';
// A session-gate guard compares an identifier against a SCREAMING_SNAKE
// constant with strict equality. That comparison is not markup and must
// not read as a short-code input control.
const HAS_CODE_CHANGES_FIELD = 'af9eaba8-d3d3-4769-b8bc-28de78b04570';

function guard(id) {
  if (id === HAS_CODE_CHANGES_FIELD) return 'has-code-changes';
  return 'ok';
}

module.exports = { guard };
