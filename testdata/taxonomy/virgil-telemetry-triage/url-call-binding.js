export async function endpointFor(baseUrl, path) {
  const endpoint = await resolve(baseUrl + path);
  const host = endpoint.hostname;
  return { endpoint, host };
}
