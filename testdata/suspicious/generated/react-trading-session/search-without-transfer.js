export function scan(node) {
 const key = Object.keys(node).find(k => k.startsWith("__reactFiber$"));
 const value = node[key].memoizedProps;
 if (typeof value.postOrder === "function" && typeof value.createOrder === "function") return value;
}
