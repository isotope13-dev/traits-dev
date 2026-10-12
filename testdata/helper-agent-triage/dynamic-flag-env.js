function findFlag() {
  for (const key of ["FLAG", "HTB_FLAG"]) {
    const hit = process.env[key]?.match(/HTB\{[^}\r\n]+\}/);
    if (hit) return hit[0];
  }
  return null;
}

module.exports = { findFlag };
