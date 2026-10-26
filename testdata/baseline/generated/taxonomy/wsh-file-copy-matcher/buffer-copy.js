function appendFrame(source, target2, start, end) {
  return toBuffer(source).copy(target2, start, end);
}
