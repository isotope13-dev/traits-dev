function update(key) {
  this /* receiver */ [key] = 1;
  delete /* operator */ this[key];
}
