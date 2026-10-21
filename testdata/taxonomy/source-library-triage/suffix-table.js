function stem(w, stem, suffixes, suffix) {
  if (w.length) w = stem + suffixes[suffix];
  return w;
}
