var fetchImpl = typeof globalThis.fetch === "function" ?
  globalThis.fetch : async function (input, init) { return await nodeFetch(input, init); };
