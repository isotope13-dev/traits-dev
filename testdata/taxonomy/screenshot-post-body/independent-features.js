import axios from 'axios';
export async function debugLogin(page) {
  await page.screenshot({ path: 'login-debug.png', fullPage: true });
}
export async function testUpload(baseUrl, fileContent) {
  const form = new FormData();
  form.append('File', new Blob([fileContent], { type: 'text/plain' }), 'test.txt');
  return axios.post(`${baseUrl}/Nodes`, form);
}
