const key = Object.keys(node).find(k => k.startsWith("__reactFiber$"));
if (typeof value.postOrder === "string" && typeof value.createOrder === "number") console.log(value);
