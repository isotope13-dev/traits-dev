function penalty(m) {
  let score = 0;
  for (const row of m) {
    let run = 0;
    for (const c of row) {
      if (c) { run++; if (run === 5) score += 3; else if (run > 5) score++; }
    }
  }
  if (score > 40) score += 40;
  return score;
}
