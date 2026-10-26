for (const [k, v] of m.entries()) {
  m.delete(k);
  m.set(k, v);
}
