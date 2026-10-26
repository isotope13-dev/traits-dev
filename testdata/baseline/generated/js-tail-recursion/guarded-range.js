// Balanced range traversal: the declaration after the guard must not hide it.
function weightRange(values, start, end, depth) {
  if (start > end) {
    return;
  }
  const middle = Math.floor((start + end) / 2);
  values[middle] = depth;
  weightRange(values, start, middle - 1, depth + 1);
  weightRange(values, middle + 1, end, depth + 1);
}
