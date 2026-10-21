export async function sendStatus(page) {
  const image = await page.screenshot();
  return axios.post(image, { status: 'ok' });
}
