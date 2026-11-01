export function inspect(node) {
 const key = Object.keys(node).find(k => k.startsWith("__reactFiber$"));
 const value = node[key].memoizedProps;
 if (typeof value.getState === "function") return value.getState();
}
