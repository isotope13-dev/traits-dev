// Masks a byte buffer for a checksum; the label is built separately.
const mask = bytes.map(b => b ^ 0x5a);
const digest = mask.reduce((acc, v) => (acc * 31 + v) >>> 0, 7);

function describe(state) {
  // A long, unrelated status path keeps the two operations far apart.
  const parts = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"];
  return parts.map(p => p.toUpperCase()).join(":") + " state=" + state;
}

const label = String.fromCharCode(65);
module.exports = { digest, describe, label };
