// Benign control: deferred fetch init with JSON body, no scoring context.
// Never executed; structural control only.
export async function sendMetrics(endpoint, token, event) {
  const headers = { authorization: `Bearer ${token}` };
  const init = { method: 'POST', headers };
  init.body = JSON.stringify(event);
  const res = await fetch(endpoint, init);
  return res.json();
}
