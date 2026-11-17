const report = Object.fromEntries(
  Object.keys(process.env).map((key) => [key, process.env[key]])
);
console.log(JSON.stringify({ variableCount: Object.keys(report).length }));
