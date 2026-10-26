export async function sendCapture(url) {
  const image = await captureScreenshots();
  return axios2.post(url, image);
}
