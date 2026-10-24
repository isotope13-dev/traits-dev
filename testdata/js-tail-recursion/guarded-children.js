// A missing child ends recursion; work after the guard does not remove it.
function coverTree(node, covered) {
  if (!node) {
    return;
  }
  const rectangles = node.rectangles;
  for (let i = 0; i < rectangles.length; ++i) {
    covered.push(rectangles[i]);
  }
  coverTree(node.north, covered);
  coverTree(node.south, covered);
}
