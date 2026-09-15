export function registryConfigured(): boolean {
  return Boolean(process.env['NPM_AUTH_TOKEN']);
}
