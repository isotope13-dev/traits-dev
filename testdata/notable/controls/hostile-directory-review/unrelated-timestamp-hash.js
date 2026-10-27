const timestamp = Date.now();
async function digestContent(bytes) {
  return crypto.subtle.digest("SHA-256", bytes);
}
