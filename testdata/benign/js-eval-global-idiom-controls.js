"""Bundled EXIF-style tag tables next to constant-eval shims: evaluating a
constant ("this", "require") cannot run a rebuilt payload."""

const TAG_TYPES = [
  1, 1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52,
];
const TAG_COUNTS = [
  0, 1, 1, 2, 4, 8, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096,
];

function tagSize(type, count) {
  let size = 0;
  for (let i = 0; i < TAG_TYPES.length; i++) {
    if (TAG_TYPES[i] === type) {
      size = TAG_COUNTS[i] * count;
    }
  }
  return size;
}

const globalObject = (0, eval)("this");
const nodeRequire = eval("require");

module.exports = { tagSize, globalObject, nodeRequire };
