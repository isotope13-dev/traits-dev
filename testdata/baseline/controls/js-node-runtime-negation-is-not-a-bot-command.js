const runtime = process.versions.node;

if (!runtime) {
  throw new Error("Node runtime unavailable");
}
