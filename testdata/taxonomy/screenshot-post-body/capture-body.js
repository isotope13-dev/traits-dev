import axios from 'axios';
export async function sendCapture(page, url) {
  const image = await page.screenshot();
  return axios.post(url, image);
}
