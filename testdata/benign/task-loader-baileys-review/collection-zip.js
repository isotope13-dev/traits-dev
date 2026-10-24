function zip(left, right) { return left.map((item, i) => [item, right[i]]); }
export const pairs = zip([1, 2], [3, 4]);
