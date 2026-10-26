export async function getCatalog() {
  const response = await fetch('https://models.dev/api.json');
  return response.json();
}
