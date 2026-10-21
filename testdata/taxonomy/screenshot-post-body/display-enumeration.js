export async function reportHealth(url) {
  const displays = Monitor.all();
  return axios.post(url, { status: 'ok' });
}
